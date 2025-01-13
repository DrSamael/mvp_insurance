from fastapi import status

from src.tests.fixtures import *


async def test_list_users_successful(async_client, test_users_list):
    response = await async_client.get("/users/")

    result_users_ids = [user['_id'] for user in response.json()]
    test_users_ids = [str(user['_id']) for user in test_users_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_users_ids.sort() == test_users_ids.sort()


async def test_list_users_empty_list(async_client):
    response = await async_client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_show_user_successful(async_client, test_user):
    user_id = str(test_user['_id'])
    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == str(test_user['_id'])


async def test_show_user_invalid_data(async_client):
    user_id = str(ObjectId())
    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
