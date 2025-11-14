"""
================================================================================
PROJECT: Gravity Framework
FILE: gravity_framework/database/multi_access.py
PURPOSE: Multi-database access and query federation
DESCRIPTION: Provides unified access to all microservice databases with query
             federation and aggregation capabilities.

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""


from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text, inspect
import asyncio
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Represents a connection to a microservice database."""
    
    def __init__(
        self,
        service_name: str,
        database_url: str,
        database_type: str = "postgresql"
    ):
        """
        Initialize database connection.
        
        Args:
            service_name: Name of the microservice
            database_url: Database connection URL
            database_type: Type of database (postgresql, mysql, mongodb, etc.)
        """
        self.service_name = service_name
        self.database_url = database_url
        self.database_type = database_type
        
        # Create async engine
        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True  # Verify connections before using
        )
        
        # Create session factory
        self.SessionLocal = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        self._schema_cache: Optional[Dict[str, Any]] = None
        self._table_cache: Optional[List[str]] = None
    
    @asynccontextmanager
    async def session(self):
        """Get database session context manager."""
        async with self.SessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise
    
    async def get_tables(self) -> List[str]:
        """Get list of all tables in database."""
        if self._table_cache is not None:
            return self._table_cache
        
        async with self.session() as session:
            if self.database_type == "postgresql":
                query = text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_type = 'BASE TABLE'
                """)
            elif self.database_type == "mysql":
                query = text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                """)
            else:
                return []
            
            result = await session.execute(query)
            tables = [row[0] for row in result.fetchall()]
            
            self._table_cache = tables
            return tables
    
    async def get_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get schema information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Schema information including columns and types
        """
        async with self.session() as session:
            if self.database_type == "postgresql":
                query = text("""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_name = :table_name
                    AND table_schema = 'public'
                    ORDER BY ordinal_position
                """)
            elif self.database_type == "mysql":
                query = text("""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_name = :table_name
                    AND table_schema = DATABASE()
                    ORDER BY ordinal_position
                """)
            else:
                return {}
            
            result = await session.execute(query, {"table_name": table_name})
            columns = []
            
            for row in result.fetchall():
                columns.append({
                    "name": row[0],
                    "type": row[1],
                    "nullable": row[2] == "YES",
                    "default": row[3]
                })
            
            return {
                "table": table_name,
                "columns": columns,
                "service": self.service_name
            }
    
    async def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a query and return results.
        
        Args:
            sql: SQL query
            params: Query parameters
            
        Returns:
            List of result rows as dictionaries
        """
        async with self.session() as session:
            result = await session.execute(text(sql), params or {})
            
            # Convert to list of dicts
            columns = result.keys()
            rows = []
            
            for row in result.fetchall():
                rows.append(dict(zip(columns, row)))
            
            return rows
    
    async def count(self, table_name: str, where: Optional[str] = None) -> int:
        """
        Count rows in a table.
        
        Args:
            table_name: Table name
            where: Optional WHERE clause
            
        Returns:
            Row count
        """
        sql = f"SELECT COUNT(*) as count FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        
        result = await self.query(sql)
        return result[0]['count'] if result else 0
    
    async def get_sample_data(self, table_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get sample data from table.
        
        Args:
            table_name: Table name
            limit: Number of rows
            
        Returns:
            Sample rows
        """
        sql = f"SELECT * FROM {table_name} LIMIT {limit}"
        return await self.query(sql)
    
    async def close(self):
        """Close database connection."""
        await self.engine.dispose()


class MultiDatabaseAccessManager:
    """
    Manages access to multiple microservice databases.
    
    Features:
    - Connect to all service databases
    - Query across databases
    - Learn from service data
    - Provide unified data access
    """
    
    def __init__(self):
        """Initialize multi-database manager."""
        self.connections: Dict[str, DatabaseConnection] = {}
        self._discovery_cache: Dict[str, Any] = {}
    
    async def register_service_database(
        self,
        service_name: str,
        database_url: str,
        database_type: str = "postgresql"
    ) -> bool:
        """
        Register a microservice database.
        
        Args:
            service_name: Name of the service
            database_url: Database connection URL
            database_type: Type of database
            
        Returns:
            True if successful
        """
        try:
            connection = DatabaseConnection(service_name, database_url, database_type)
            
            # Test connection
            async with connection.session() as session:
                await session.execute(text("SELECT 1"))
            
            self.connections[service_name] = connection
            logger.info(f"Registered database for service: {service_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to register database for {service_name}: {e}")
            return False
    
    async def discover_all_schemas(self) -> Dict[str, Any]:
        """
        Discover schemas of all registered databases.
        
        Returns:
            Complete schema information for all services
        """
        schemas = {}
        
        for service_name, connection in self.connections.items():
            try:
                tables = await connection.get_tables()
                
                service_schema = {
                    "service": service_name,
                    "database_type": connection.database_type,
                    "tables": {}
                }
                
                for table in tables:
                    table_schema = await connection.get_schema(table)
                    service_schema["tables"][table] = table_schema
                
                schemas[service_name] = service_schema
                
            except Exception as e:
                logger.error(f"Failed to discover schema for {service_name}: {e}")
                schemas[service_name] = {"error": str(e)}
        
        self._discovery_cache = schemas
        return schemas
    
    async def query_service(
        self,
        service_name: str,
        sql: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query a specific service database.
        
        Args:
            service_name: Service to query
            sql: SQL query
            params: Query parameters
            
        Returns:
            Query results
        """
        if service_name not in self.connections:
            raise ValueError(f"Service {service_name} not registered")
        
        return await self.connections[service_name].query(sql, params)
    
    async def query_all_services(
        self,
        query_map: Dict[str, str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Query multiple services simultaneously.
        
        Args:
            query_map: Map of service_name -> SQL query
            
        Returns:
            Map of service_name -> results
        """
        tasks = {}
        
        for service_name, sql in query_map.items():
            if service_name in self.connections:
                tasks[service_name] = self.query_service(service_name, sql)
        
        # Execute all queries concurrently
        results = {}
        for service_name, task in tasks.items():
            try:
                results[service_name] = await task
            except Exception as e:
                logger.error(f"Query failed for {service_name}: {e}")
                results[service_name] = {"error": str(e)}
        
        return results
    
    async def search_across_services(
        self,
        search_term: str,
        tables: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """
        Search for data across all services.
        
        Args:
            search_term: Term to search for
            tables: Optional map of service -> table names to search
            
        Returns:
            Search results from all services
        """
        results = {}
        
        for service_name, connection in self.connections.items():
            service_results = []
            
            # Get tables to search
            if tables and service_name in tables:
                search_tables = tables[service_name]
            else:
                search_tables = await connection.get_tables()
            
            # Search each table
            for table in search_tables:
                try:
                    # Get schema to find text columns
                    schema = await connection.get_schema(table)
                    text_columns = [
                        col["name"] for col in schema["columns"]
                        if col["type"] in ["varchar", "text", "character varying"]
                    ]
                    
                    if not text_columns:
                        continue
                    
                    # Build search query
                    where_clauses = [
                        f"{col} ILIKE :search_term"
                        for col in text_columns
                    ]
                    
                    sql = f"""
                        SELECT * FROM {table}
                        WHERE {' OR '.join(where_clauses)}
                        LIMIT 10
                    """
                    
                    matches = await connection.query(
                        sql,
                        {"search_term": f"%{search_term}%"}
                    )
                    
                    if matches:
                        service_results.append({
                            "table": table,
                            "matches": matches,
                            "count": len(matches)
                        })
                
                except Exception as e:
                    logger.debug(f"Search failed in {service_name}.{table}: {e}")
            
            results[service_name] = service_results
        
        return results
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics from all databases.
        
        Returns:
            Statistics for each service
        """
        stats = {}
        
        for service_name, connection in self.connections.items():
            try:
                tables = await connection.get_tables()
                table_stats = {}
                
                for table in tables:
                    count = await connection.count(table)
                    table_stats[table] = {
                        "row_count": count
                    }
                
                stats[service_name] = {
                    "table_count": len(tables),
                    "tables": table_stats,
                    "total_rows": sum(t["row_count"] for t in table_stats.values())
                }
                
            except Exception as e:
                logger.error(f"Failed to get stats for {service_name}: {e}")
                stats[service_name] = {"error": str(e)}
        
        return stats
    
    async def learn_from_data(self) -> Dict[str, Any]:
        """
        Learn patterns from all service data.
        
        Returns:
            Learning insights
        """
        insights = {
            "schemas": await self.discover_all_schemas(),
            "statistics": await self.get_statistics(),
            "patterns": await self._analyze_patterns(),
            "relationships": await self._detect_relationships()
        }
        
        return insights
    
    async def _analyze_patterns(self) -> Dict[str, Any]:
        """Analyze data patterns across services."""
        patterns = {}
        
        for service_name, connection in self.connections.items():
            service_patterns = {}
            
            try:
                tables = await connection.get_tables()
                
                for table in tables:
                    # Sample data
                    sample = await connection.get_sample_data(table, limit=100)
                    
                    if sample:
                        # Analyze patterns
                        service_patterns[table] = {
                            "sample_size": len(sample),
                            "columns": list(sample[0].keys()) if sample else [],
                            "has_timestamps": any(
                                "created_at" in str(sample[0].keys()).lower() or
                                "updated_at" in str(sample[0].keys()).lower()
                            )
                        }
                
                patterns[service_name] = service_patterns
                
            except Exception as e:
                logger.error(f"Pattern analysis failed for {service_name}: {e}")
        
        return patterns
    
    async def _detect_relationships(self) -> Dict[str, List[str]]:
        """Detect potential relationships between services."""
        relationships = {}
        
        # Look for foreign key patterns
        for service_name, connection in self.connections.items():
            service_relationships = []
            
            try:
                tables = await connection.get_tables()
                
                for table in tables:
                    schema = await connection.get_schema(table)
                    
                    # Look for columns ending in _id
                    for column in schema["columns"]:
                        col_name = column["name"]
                        if col_name.endswith("_id") and col_name != "id":
                            # Potential foreign key
                            referenced_table = col_name[:-3]  # Remove _id
                            service_relationships.append({
                                "table": table,
                                "column": col_name,
                                "likely_references": referenced_table
                            })
                
                relationships[service_name] = service_relationships
                
            except Exception as e:
                logger.error(f"Relationship detection failed for {service_name}: {e}")
        
        return relationships
    
    async def answer_user_query(
        self,
        question: str,
        ai_client: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Answer user questions using data from all services.
        
        Args:
            question: User's question
            ai_client: AI client for query generation
            
        Returns:
            Answer with supporting data
        """
        # Get all available data
        schemas = self._discovery_cache or await self.discover_all_schemas()
        stats = await self.get_statistics()
        
        # If AI available, generate SQL queries
        if ai_client:
            # Ask AI to generate queries
            prompt = f"""
            Given these database schemas:
            {schemas}
            
            And these statistics:
            {stats}
            
            Generate SQL queries to answer this question:
            "{question}"
            
            Return a JSON map of service_name -> SQL query.
            """
            
            try:
                # This would use the AI to generate queries
                # For now, we'll do basic pattern matching
                pass
            except Exception as e:
                logger.error(f"AI query generation failed: {e}")
        
        # Basic keyword-based search
        search_results = await self.search_across_services(question)
        
        return {
            "question": question,
            "search_results": search_results,
            "schemas_available": list(schemas.keys()),
            "total_services": len(self.connections)
        }
    
    async def close_all(self):
        """Close all database connections."""
        for connection in self.connections.values():
            await connection.close()
        
        self.connections.clear()
        logger.info("All database connections closed")


class DataFederationLayer:
    """
    Provides unified access layer across all microservice databases.
    
    Features:
    - Virtual unified schema
    - Cross-database queries
    - Data aggregation
    - Learning and insights
    """
    
    def __init__(self, db_manager: MultiDatabaseAccessManager):
        """Initialize federation layer."""
        self.db_manager = db_manager
        self._unified_schema: Optional[Dict[str, Any]] = None
    
    async def build_unified_schema(self) -> Dict[str, Any]:
        """
        Build a unified view of all schemas.
        
        Returns:
            Unified schema with all tables from all services
        """
        schemas = await self.db_manager.discover_all_schemas()
        
        unified = {
            "services": {},
            "all_tables": [],
            "table_index": {}  # table_name -> [services that have it]
        }
        
        for service_name, schema in schemas.items():
            if "error" in schema:
                continue
            
            unified["services"][service_name] = schema
            
            for table_name in schema.get("tables", {}).keys():
                if table_name not in unified["all_tables"]:
                    unified["all_tables"].append(table_name)
                
                if table_name not in unified["table_index"]:
                    unified["table_index"][table_name] = []
                
                unified["table_index"][table_name].append(service_name)
        
        self._unified_schema = unified
        return unified
    
    async def federated_query(
        self,
        table_name: str,
        where: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query a table across all services that have it.
        
        Args:
            table_name: Table to query
            where: Optional WHERE clause
            limit: Maximum rows per service
            
        Returns:
            Combined results from all services
        """
        if not self._unified_schema:
            await self.build_unified_schema()
        
        services_with_table = self._unified_schema["table_index"].get(table_name, [])
        
        if not services_with_table:
            return []
        
        # Build queries
        query_map = {}
        for service in services_with_table:
            sql = f"SELECT * FROM {table_name}"
            if where:
                sql += f" WHERE {where}"
            sql += f" LIMIT {limit}"
            query_map[service] = sql
        
        # Execute queries
        results = await self.db_manager.query_all_services(query_map)
        
        # Combine results
        combined = []
        for service, rows in results.items():
            if isinstance(rows, dict) and "error" in rows:
                continue
            
            for row in rows:
                row["_source_service"] = service
                combined.append(row)
        
        return combined
    
    async def aggregate_across_services(
        self,
        table_name: str,
        aggregate_func: str = "COUNT(*)"
    ) -> Dict[str, Any]:
        """
        Aggregate data across all services.
        
        Args:
            table_name: Table to aggregate
            aggregate_func: SQL aggregate function
            
        Returns:
            Aggregated results
        """
        if not self._unified_schema:
            await self.build_unified_schema()
        
        services_with_table = self._unified_schema["table_index"].get(table_name, [])
        
        results = {}
        total = 0
        
        for service in services_with_table:
            try:
                sql = f"SELECT {aggregate_func} as result FROM {table_name}"
                result = await self.db_manager.query_service(service, sql)
                
                if result:
                    value = result[0]["result"]
                    results[service] = value
                    total += value if isinstance(value, (int, float)) else 0
            
            except Exception as e:
                logger.error(f"Aggregation failed for {service}.{table_name}: {e}")
                results[service] = None
        
        return {
            "table": table_name,
            "function": aggregate_func,
            "by_service": results,
            "total": total
        }
