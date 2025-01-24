import pytest
from fastapi import status

from src.tests.fixtures import *
from src.auth.utils import create_token
from src.exceptions import (INVALID_LOGIN_DATA_EXCEPTION, CREDENTIALS_INVALID_EXCEPTION, USER_NOT_FOUND_EXCEPTION,
                            TOKEN_EXPIRE_EXCEPTION)


@pytest.mark.asyncio(loop_scope="session")
async def test_login_successful(async_client, test_user_with_encrypted_password):
    login_data = {
        "username": test_user_with_encrypted_password["email"],
        "password": "123123"
    }
    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert "access_token" in result
    assert "refresh_token" in result


@pytest.mark.asyncio(loop_scope="session")
async def test_login_invalid_password(async_client, test_user_with_encrypted_password):
    login_data = {
        "username": test_user_with_encrypted_password["email"],
        "password": "wrong_password"
    }
    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == INVALID_LOGIN_DATA_EXCEPTION.detail


@pytest.mark.asyncio(loop_scope="session")
async def test_login_invalid_email(async_client, test_user_with_encrypted_password):
    login_data = {
        "username": 'wrong_email',
        "password": "123123"
    }
    response = await async_client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == INVALID_LOGIN_DATA_EXCEPTION.detail


@pytest.mark.asyncio(loop_scope="session")
async def test_login_blank_data(async_client):
    response = await async_client.post("/auth/login", data={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(loop_scope="session")
async def test_get_me_successful(async_client, test_user):
    access_token = await create_token(test_user["_id"], None, 'access_token')
    response = await async_client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    result_user = response.json()

    assert response.status_code == status.HTTP_200_OK

    test_user['_id'] = str(test_user['_id'])
    for key in test_user:
        if key != 'password':
            assert test_user[key] == result_user[key]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_me_unauthorized(async_client):
    response = await async_client.get("/auth/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio(loop_scope="session")
async def test_get_me_invalid_user_id(async_client):
    access_token = await create_token(ObjectId(), None, 'access_token')
    response = await async_client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == CREDENTIALS_INVALID_EXCEPTION.detail


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_token_successful(async_client, test_user):
    refresh_token = await create_token(test_user["_id"], 15, 'refresh_token')
    response = await async_client.get("/auth/refresh-token", headers={"Authorization": f"Bearer {refresh_token}"})

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert "access_token" in result
    assert "refresh_token" in result


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_token_blank(async_client):
    response = await async_client.get("/auth/refresh-token")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_token_invalid_user_id(async_client):
    refresh_token = await create_token(ObjectId(), 15, 'refresh_token')
    response = await async_client.get("/auth/refresh-token", headers={"Authorization": f"Bearer {refresh_token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == CREDENTIALS_INVALID_EXCEPTION.detail


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_token_expired(async_client, test_user):
    expired_token = await create_token(test_user["_id"], -15, 'refresh_token')
    response = await async_client.get("/auth/refresh-token", headers={"Authorization": f"Bearer {expired_token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == TOKEN_EXPIRE_EXCEPTION.detail


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_token_invalid(async_client):
    response = await async_client.get("/auth/refresh-token", headers={"Authorization": "Bearer invalid_refresh_token"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == CREDENTIALS_INVALID_EXCEPTION.detail
