"""
================================================================================
PROJECT: Gravity Framework
FILE: examples/sample-auth-service/tests/test_auth.py
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

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_register_new_user(client: AsyncClient):
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "password" not in data
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login."""
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    """Test getting current user information."""
    # First, login to get token
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Then, get current user
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "email" in data
    assert "username" in data
    assert "is_active" in data


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    """Test logout."""
    # Login first
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Logout
    response = await client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
