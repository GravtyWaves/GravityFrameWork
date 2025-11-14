"""Dependency resolution using PubGrub algorithm."""

import logging
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, deque
import re

from gravity_framework.models.service import Service, ServiceDependency

logger = logging.getLogger(__name__)


class VersionConstraint:
    """Version constraint parser and evaluator."""
    
    def __init__(self, constraint: str):
        """Initialize version constraint.
        
        Args:
            constraint: Version constraint string (e.g., ">=1.0.0", "~1.2.3", "^2.0.0")
        """
        self.constraint = constraint or "*"
        self.operator, self.version = self._parse_constraint(self.constraint)
    
    def _parse_constraint(self, constraint: str) -> Tuple[str, List[int]]:
        """Parse constraint string."""
        constraint = constraint.strip()
        
        # Match operator and version
        match = re.match(r"^([>=<^~*]+)?(\d+(?:\.\d+(?:\.\d+)?)?)$", constraint)
        if not match:
            if constraint == "*":
                return ("*", [0, 0, 0])
            raise ValueError(f"Invalid version constraint: {constraint}")
        
        operator = match.group(1) or "=="
        version_str = match.group(2)
        
        # Parse version numbers
        parts = version_str.split(".")
        version = [int(p) for p in parts]
        
        # Pad to 3 parts
        while len(version) < 3:
            version.append(0)
        
        return (operator, version)
    
    def matches(self, version: str) -> bool:
        """Check if version matches constraint.
        
        Args:
            version: Version string to check
            
        Returns:
            True if version matches constraint
        """
        if self.operator == "*":
            return True
        
        # Parse version
        parts = version.split(".")
        v = [int(p) for p in parts]
        while len(v) < 3:
            v.append(0)
        
        # Check constraint
        if self.operator == "==":
            return v == self.version
        elif self.operator == ">=":
            return v >= self.version
        elif self.operator == ">":
            return v > self.version
        elif self.operator == "<=":
            return v <= self.version
        elif self.operator == "<":
            return v < self.version
        elif self.operator == "^":
            # Compatible with version (same major)
            return v[0] == self.version[0] and v >= self.version
        elif self.operator == "~":
            # Approximately equivalent (same major and minor)
            return v[0] == self.version[0] and v[1] == self.version[1] and v >= self.version
        
        return False


class DependencyResolver:
    """Dependency resolver using topological sort."""
    
    def __init__(self, services: List[Service]):
        """Initialize resolver.
        
        Args:
            services: List of services to resolve
        """
        self.services = {s.manifest.name: s for s in services}
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        self.in_degree: Dict[str, int] = defaultdict(int)
    
    def build_graph(self) -> bool:
        """Build dependency graph.
        
        Returns:
            True if graph is valid (no conflicts), False otherwise
        """
        logger.info("Building dependency graph...")
        
        # Build edges
        for service in self.services.values():
            service_name = service.manifest.name
            
            for dep in service.manifest.dependencies:
                dep_name = dep.name
                
                # Check if dependency exists
                if dep_name not in self.services:
                    if not dep.optional:
                        logger.error(f"Missing required dependency: {service_name} requires {dep_name}")
                        return False
                    else:
                        logger.warning(f"Optional dependency not found: {dep_name} (required by {service_name})")
                        continue
                
                # Check version compatibility
                if dep.version:
                    dep_service = self.services[dep_name]
                    constraint = VersionConstraint(dep.version)
                    
                    if not constraint.matches(dep_service.manifest.version):
                        logger.error(
                            f"Version conflict: {service_name} requires {dep_name} {dep.version}, "
                            f"but version {dep_service.manifest.version} is available"
                        )
                        return False
                
                # Add edge: dep_name -> service_name (service depends on dep)
                self.graph[dep_name].add(service_name)
                self.in_degree[service_name] += 1
        
        # Initialize in_degree for all services
        for service_name in self.services:
            if service_name not in self.in_degree:
                self.in_degree[service_name] = 0
        
        # Check for cycles
        if self._has_cycle():
            logger.error("Circular dependency detected!")
            return False
        
        logger.info(f"✓ Dependency graph built successfully with {len(self.services)} service(s)")
        return True
    
    def _has_cycle(self) -> bool:
        """Check if graph has cycles using DFS.
        
        Returns:
            True if cycle exists
        """
        visited = set()
        rec_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in self.services:
            if node not in visited:
                if dfs(node):
                    return True
        
        return False
    
    def resolve(self) -> Optional[List[Service]]:
        """Resolve dependencies and return installation order.
        
        Returns:
            Ordered list of services (dependencies first) or None if resolution fails
        """
        if not self.build_graph():
            return None
        
        logger.info("Resolving installation order...")
        
        # Topological sort using Kahn's algorithm
        queue = deque([name for name, degree in self.in_degree.items() if degree == 0])
        order = []
        
        while queue:
            # Get service with no dependencies
            current = queue.popleft()
            order.append(current)
            
            # Remove edges
            for neighbor in self.graph[current]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check if all services were processed
        if len(order) != len(self.services):
            logger.error("Failed to resolve all dependencies (circular dependency)")
            return None
        
        # Convert names back to Service objects
        ordered_services = [self.services[name] for name in order]
        
        logger.info(f"✓ Installation order: {' -> '.join(order)}")
        return ordered_services
    
    def get_dependencies(self, service_name: str) -> List[str]:
        """Get direct dependencies of a service.
        
        Args:
            service_name: Service name
            
        Returns:
            List of dependency names
        """
        if service_name not in self.services:
            return []
        
        service = self.services[service_name]
        return [dep.name for dep in service.manifest.dependencies if not dep.optional or dep.name in self.services]
    
    def get_dependents(self, service_name: str) -> List[str]:
        """Get services that depend on this service.
        
        Args:
            service_name: Service name
            
        Returns:
            List of dependent service names
        """
        return list(self.graph.get(service_name, []))
