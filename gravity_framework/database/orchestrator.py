"""Database orchestration and management."""

import logging
from typing import Dict, List, Optional
from pathlib import Path
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text
import asyncpg
import aiomysql
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as aioredis

from gravity_framework.models.service import Service, DatabaseRequirement, DatabaseType

logger = logging.getLogger(__name__)


class DatabaseOrchestrator:
    """Database orchestrator for creating and managing databases."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize database orchestrator.
        
        Args:
            config: Database configuration
        """
        self.config = config or {}
        self.engines: Dict[str, AsyncEngine] = {}
        self.connections: Dict[str, any] = {}
        
        # Default configurations
        self.postgres_host = self.config.get("postgres_host", "localhost")
        self.postgres_port = self.config.get("postgres_port", 5432)
        self.postgres_user = self.config.get("postgres_user", "postgres")
        self.postgres_password = self.config.get("postgres_password", "postgres")
        
        self.mysql_host = self.config.get("mysql_host", "localhost")
        self.mysql_port = self.config.get("mysql_port", 3306)
        self.mysql_user = self.config.get("mysql_user", "root")
        self.mysql_password = self.config.get("mysql_password", "root")
        
        self.mongodb_host = self.config.get("mongodb_host", "localhost")
        self.mongodb_port = self.config.get("mongodb_port", 27017)
        self.mongodb_user = self.config.get("mongodb_user", None)
        self.mongodb_password = self.config.get("mongodb_password", None)
        
        self.redis_host = self.config.get("redis_host", "localhost")
        self.redis_port = self.config.get("redis_port", 6379)
        self.redis_password = self.config.get("redis_password", None)
    
    async def setup_databases(self, service: Service) -> bool:
        """Setup all required databases for a service.
        
        Args:
            service: Service instance
            
        Returns:
            True if all databases were created successfully
        """
        if not service.manifest.databases:
            logger.debug(f"No databases required for {service.manifest.name}")
            return True
        
        logger.info(f"Setting up {len(service.manifest.databases)} database(s) for {service.manifest.name}")
        
        success = True
        for db_req in service.manifest.databases:
            try:
                if db_req.type == DatabaseType.POSTGRESQL:
                    await self._create_postgres_db(db_req)
                elif db_req.type == DatabaseType.MYSQL:
                    await self._create_mysql_db(db_req)
                elif db_req.type == DatabaseType.MONGODB:
                    await self._create_mongodb(db_req)
                elif db_req.type == DatabaseType.REDIS:
                    await self._setup_redis(db_req)
                
                service.created_databases.append(db_req.name)
                logger.info(f"✓ Created {db_req.type.value} database: {db_req.name}")
                
            except Exception as e:
                logger.error(f"✗ Failed to create {db_req.type.value} database {db_req.name}: {e}")
                success = False
        
        return success
    
    async def _create_postgres_db(self, db_req: DatabaseRequirement) -> None:
        """Create PostgreSQL database.
        
        Args:
            db_req: Database requirement
        """
        # Connect to postgres database
        conn = await asyncpg.connect(
            host=self.postgres_host,
            port=self.postgres_port,
            user=self.postgres_user,
            password=self.postgres_password,
            database="postgres"
        )
        
        try:
            # Check if database exists
            result = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1",
                db_req.name
            )
            
            if result:
                logger.info(f"PostgreSQL database {db_req.name} already exists")
                return
            
            # Create database
            await conn.execute(f'CREATE DATABASE "{db_req.name}"')
            
            # Install extensions if needed
            if db_req.extensions:
                db_conn = await asyncpg.connect(
                    host=self.postgres_host,
                    port=self.postgres_port,
                    user=self.postgres_user,
                    password=self.postgres_password,
                    database=db_req.name
                )
                
                try:
                    for extension in db_req.extensions:
                        await db_conn.execute(f'CREATE EXTENSION IF NOT EXISTS "{extension}"')
                        logger.debug(f"Installed extension: {extension}")
                finally:
                    await db_conn.close()
        
        finally:
            await conn.close()
    
    async def _create_mysql_db(self, db_req: DatabaseRequirement) -> None:
        """Create MySQL database.
        
        Args:
            db_req: Database requirement
        """
        # Connect to MySQL
        conn = await aiomysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password
        )
        
        try:
            async with conn.cursor() as cursor:
                # Check if database exists
                await cursor.execute(
                    "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
                    (db_req.name,)
                )
                result = await cursor.fetchone()
                
                if result:
                    logger.info(f"MySQL database {db_req.name} already exists")
                    return
                
                # Create database with charset and collation
                charset = db_req.charset or "utf8mb4"
                collation = db_req.collation or "utf8mb4_unicode_ci"
                
                await cursor.execute(
                    f"CREATE DATABASE `{db_req.name}` "
                    f"CHARACTER SET {charset} COLLATE {collation}"
                )
                await conn.commit()
        
        finally:
            conn.close()
    
    async def _create_mongodb(self, db_req: DatabaseRequirement) -> None:
        """Create MongoDB database.
        
        Args:
            db_req: Database requirement
        """
        # MongoDB creates databases automatically when data is written
        # We just verify connection and create a dummy collection
        
        if self.mongodb_user and self.mongodb_password:
            uri = f"mongodb://{self.mongodb_user}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}"
        else:
            uri = f"mongodb://{self.mongodb_host}:{self.mongodb_port}"
        
        client = AsyncIOMotorClient(uri)
        
        try:
            # Access database
            db = client[db_req.name]
            
            # Create a collection to ensure database is created
            await db.create_collection("_gravity_init")
            
            # Verify connection
            await db.command("ping")
            
            logger.debug(f"MongoDB database {db_req.name} initialized")
        
        finally:
            client.close()
    
    async def _setup_redis(self, db_req: DatabaseRequirement) -> None:
        """Setup Redis connection.
        
        Args:
            db_req: Database requirement
        """
        # Redis doesn't have databases in the traditional sense
        # We just verify connection
        
        redis_client = await aioredis.from_url(
            f"redis://{self.redis_host}:{self.redis_port}",
            password=self.redis_password,
            decode_responses=True
        )
        
        try:
            # Ping to verify connection
            await redis_client.ping()
            logger.debug(f"Redis connection verified for {db_req.name}")
        
        finally:
            await redis_client.close()
    
    async def get_connection_string(self, db_req: DatabaseRequirement) -> str:
        """Get connection string for a database.
        
        Args:
            db_req: Database requirement
            
        Returns:
            Connection string
        """
        if db_req.type == DatabaseType.POSTGRESQL:
            return (
                f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{db_req.name}"
            )
        elif db_req.type == DatabaseType.MYSQL:
            charset = db_req.charset or "utf8mb4"
            return (
                f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@"
                f"{self.mysql_host}:{self.mysql_port}/{db_req.name}?charset={charset}"
            )
        elif db_req.type == DatabaseType.MONGODB:
            if self.mongodb_user and self.mongodb_password:
                return (
                    f"mongodb://{self.mongodb_user}:{self.mongodb_password}@"
                    f"{self.mongodb_host}:{self.mongodb_port}/{db_req.name}"
                )
            return f"mongodb://{self.mongodb_host}:{self.mongodb_port}/{db_req.name}"
        elif db_req.type == DatabaseType.REDIS:
            return f"redis://{self.redis_host}:{self.redis_port}"
        
        raise ValueError(f"Unknown database type: {db_req.type}")
    
    async def cleanup_databases(self, service: Service) -> bool:
        """Cleanup databases for a service.
        
        Args:
            service: Service instance
            
        Returns:
            True if cleanup was successful
        """
        if not service.created_databases:
            return True
        
        logger.info(f"Cleaning up databases for {service.manifest.name}")
        
        success = True
        for db_name in service.created_databases:
            try:
                # Find database requirement
                db_req = next(
                    (db for db in service.manifest.databases if db.name == db_name),
                    None
                )
                
                if not db_req:
                    continue
                
                if db_req.type == DatabaseType.POSTGRESQL:
                    await self._drop_postgres_db(db_name)
                elif db_req.type == DatabaseType.MYSQL:
                    await self._drop_mysql_db(db_name)
                elif db_req.type == DatabaseType.MONGODB:
                    await self._drop_mongodb(db_name)
                
                logger.info(f"✓ Dropped database: {db_name}")
                
            except Exception as e:
                logger.error(f"✗ Failed to drop database {db_name}: {e}")
                success = False
        
        return success
    
    async def _drop_postgres_db(self, db_name: str) -> None:
        """Drop PostgreSQL database."""
        conn = await asyncpg.connect(
            host=self.postgres_host,
            port=self.postgres_port,
            user=self.postgres_user,
            password=self.postgres_password,
            database="postgres"
        )
        
        try:
            await conn.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
        finally:
            await conn.close()
    
    async def _drop_mysql_db(self, db_name: str) -> None:
        """Drop MySQL database."""
        conn = await aiomysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password
        )
        
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
                await conn.commit()
        finally:
            conn.close()
    
    async def _drop_mongodb(self, db_name: str) -> None:
        """Drop MongoDB database."""
        if self.mongodb_user and self.mongodb_password:
            uri = f"mongodb://{self.mongodb_user}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}"
        else:
            uri = f"mongodb://{self.mongodb_host}:{self.mongodb_port}"
        
        client = AsyncIOMotorClient(uri)
        
        try:
            await client.drop_database(db_name)
        finally:
            client.close()
