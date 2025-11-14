"""
================================================================================
PROJECT: Gravity Framework
FILE: tests/test_resolver.py
PURPOSE: Framework component
DESCRIPTION: Component of the Gravity Framework for microservices orchestration

AUTHOR: Gravity Framework Team
EMAIL: team@gravityframework.dev
LICENSE: MIT
CREATED: 2025-11-13
MODIFIED: 2025-11-14

COPYRIGHT: (c) 2025 Gravity Framework Team
REPOSITORY: https://github.com/GravtyWaves/GravityFrameWork
================================================================================
"""

    manifest = ServiceManifest(
        name="service-a",
        version="1.0.0",
        repository="https://github.com/test/service-a",
        dependencies=[
            ServiceDependency(name="service-b", version=">=1.0.0")
        ]
    )
    return Service(manifest=manifest)


@pytest.fixture
def service_b():
    """Create service B."""
    manifest = ServiceManifest(
        name="service-b",
        version="1.5.0",
        repository="https://github.com/test/service-b",
        dependencies=[
            ServiceDependency(name="service-c", version="^1.0.0")
        ]
    )
    return Service(manifest=manifest)


@pytest.fixture
def service_c():
    """Create service C."""
    manifest = ServiceManifest(
        name="service-c",
        version="1.2.0",
        repository="https://github.com/test/service-c",
        dependencies=[]
    )
    return Service(manifest=manifest)


class TestVersionConstraint:
    """Test VersionConstraint class."""
    
    def test_parse_equals(self):
        """Test parsing == constraint."""
        constraint = VersionConstraint("==1.0.0")
        assert constraint.matches("1.0.0")
        assert not constraint.matches("1.0.1")
    
    def test_parse_greater_or_equal(self):
        """Test parsing >= constraint."""
        constraint = VersionConstraint(">=1.0.0")
        assert constraint.matches("1.0.0")
        assert constraint.matches("1.5.0")
        assert constraint.matches("2.0.0")
        assert not constraint.matches("0.9.0")
    
    def test_parse_caret(self):
        """Test parsing ^ constraint (compatible)."""
        constraint = VersionConstraint("^1.2.3")
        assert constraint.matches("1.2.3")
        assert constraint.matches("1.5.0")
        assert constraint.matches("1.9.9")
        assert not constraint.matches("2.0.0")
        assert not constraint.matches("0.9.0")
    
    def test_parse_tilde(self):
        """Test parsing ~ constraint (approximately)."""
        constraint = VersionConstraint("~1.2.3")
        assert constraint.matches("1.2.3")
        assert constraint.matches("1.2.9")
        assert not constraint.matches("1.3.0")
        assert not constraint.matches("2.0.0")
    
    def test_parse_wildcard(self):
        """Test parsing * constraint (any version)."""
        constraint = VersionConstraint("*")
        assert constraint.matches("0.0.1")
        assert constraint.matches("1.0.0")
        assert constraint.matches("99.99.99")


class TestDependencyResolver:
    """Test DependencyResolver class."""
    
    def test_resolver_initialization(self, service_a, service_b):
        """Test resolver initializes correctly."""
        resolver = DependencyResolver([service_a, service_b])
        assert len(resolver.services) == 2
        assert "service-a" in resolver.services
        assert "service-b" in resolver.services
    
    def test_build_graph_simple(self, service_a, service_b, service_c):
        """Test building dependency graph."""
        resolver = DependencyResolver([service_a, service_b, service_c])
        result = resolver.build_graph()
        
        assert result is True
        assert "service-a" in resolver.graph["service-b"]
        assert "service-b" in resolver.graph["service-c"]
    
    def test_build_graph_missing_dependency(self, service_a):
        """Test building graph with missing dependency."""
        resolver = DependencyResolver([service_a])
        result = resolver.build_graph()
        
        assert result is False
    
    def test_build_graph_circular_dependency(self):
        """Test detecting circular dependency."""
        # A -> B -> C -> A
        manifest_a = ServiceManifest(
            name="service-a",
            version="1.0.0",
            repository="repo",
            dependencies=[ServiceDependency(name="service-b")]
        )
        manifest_b = ServiceManifest(
            name="service-b",
            version="1.0.0",
            repository="repo",
            dependencies=[ServiceDependency(name="service-c")]
        )
        manifest_c = ServiceManifest(
            name="service-c",
            version="1.0.0",
            repository="repo",
            dependencies=[ServiceDependency(name="service-a")]
        )
        
        services = [
            Service(manifest=manifest_a),
            Service(manifest=manifest_b),
            Service(manifest=manifest_c)
        ]
        
        resolver = DependencyResolver(services)
        result = resolver.build_graph()
        
        assert result is False
    
    def test_resolve_correct_order(self, service_a, service_b, service_c):
        """Test resolving correct installation order."""
        resolver = DependencyResolver([service_a, service_b, service_c])
        ordered_services = resolver.resolve()
        
        assert ordered_services is not None
        assert len(ordered_services) == 3
        
        # service-c should come first (no dependencies)
        # service-b depends on service-c
        # service-a depends on service-b
        names = [s.manifest.name for s in ordered_services]
        assert names.index("service-c") < names.index("service-b")
        assert names.index("service-b") < names.index("service-a")
    
    def test_get_dependencies(self, service_a, service_b, service_c):
        """Test getting direct dependencies."""
        resolver = DependencyResolver([service_a, service_b, service_c])
        resolver.build_graph()
        
        deps = resolver.get_dependencies("service-a")
        assert "service-b" in deps
        
        deps = resolver.get_dependencies("service-c")
        assert len(deps) == 0
    
    def test_get_dependents(self, service_a, service_b, service_c):
        """Test getting services that depend on a service."""
        resolver = DependencyResolver([service_a, service_b, service_c])
        resolver.build_graph()
        
        dependents = resolver.get_dependents("service-b")
        assert "service-a" in dependents
        
        dependents = resolver.get_dependents("service-a")
        assert len(dependents) == 0
    
    def test_version_conflict(self):
        """Test detecting version conflicts."""
        manifest_a = ServiceManifest(
            name="service-a",
            version="1.0.0",
            repository="repo",
            dependencies=[ServiceDependency(name="service-b", version=">=2.0.0")]
        )
        manifest_b = ServiceManifest(
            name="service-b",
            version="1.0.0",  # Lower than required
            repository="repo"
        )
        
        services = [
            Service(manifest=manifest_a),
            Service(manifest=manifest_b)
        ]
        
        resolver = DependencyResolver(services)
        result = resolver.build_graph()
        
        assert result is False
    
    def test_optional_dependency_missing(self):
        """Test handling missing optional dependency."""
        manifest = ServiceManifest(
            name="service-a",
            version="1.0.0",
            repository="repo",
            dependencies=[
                ServiceDependency(name="service-b", optional=True)
            ]
        )
        
        service = Service(manifest=manifest)
        resolver = DependencyResolver([service])
        result = resolver.build_graph()
        
        # Should succeed because dependency is optional
        assert result is True
