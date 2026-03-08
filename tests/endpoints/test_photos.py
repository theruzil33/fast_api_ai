from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

MOCK_PHOTO = {
    "id": 1,
    "owner_id": 123,
    "date": 1700000000,
    "text": "",
    "sizes": [{"type": "x", "url": "https://example.com/photo.jpg", "width": 604, "height": 453}],
}


def test_get_user_photos_success():
    # Проверяет успешный ответ: статус 200, корректные user_id, total=1 и id первого фото
    with patch("app.api.v1.endpoints.photos.fetch_all_photos", new=AsyncMock(return_value=[MOCK_PHOTO])):
        response = client.get("/api/v1/photos/123")

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 123
    assert data["total"] == 1
    assert len(data["photos"]) == 1
    assert data["photos"][0]["id"] == 1


def test_get_user_photos_empty():
    # Проверяет, что при отсутствии фото у пользователя возвращается статус 200 с total=0 и пустым списком
    with patch("app.api.v1.endpoints.photos.fetch_all_photos", new=AsyncMock(return_value=[])):
        response = client.get("/api/v1/photos/123")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["photos"] == []


def test_get_user_photos_multiple():
    # Проверяет, что при нескольких фото total и длина списка photos совпадают с количеством возвращённых элементов
    photos = [
        {**MOCK_PHOTO, "id": i, "owner_id": 123}
        for i in range(1, 6)
    ]
    with patch("app.api.v1.endpoints.photos.fetch_all_photos", new=AsyncMock(return_value=photos)):
        response = client.get("/api/v1/photos/123")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["photos"]) == 5


def test_get_user_photos_vk_api_error():
    # Проверяет, что ошибка VK API (ValueError) возвращает статус 400 с текстом ошибки в detail
    with patch(
        "app.api.v1.endpoints.photos.fetch_all_photos",
        new=AsyncMock(side_effect=ValueError("VK API error 15: Access denied")),
    ):
        response = client.get("/api/v1/photos/123")

    assert response.status_code == 400
    assert "Access denied" in response.json()["detail"]


def test_get_user_photos_network_error():
    # Проверяет, что сетевая ошибка (Exception) возвращает статус 502 с сообщением "VK API недоступен"
    with patch(
        "app.api.v1.endpoints.photos.fetch_all_photos",
        new=AsyncMock(side_effect=Exception("Connection timeout")),
    ):
        response = client.get("/api/v1/photos/123")

    assert response.status_code == 502
    assert "VK API недоступен" in response.json()["detail"]


def test_get_user_photos_invalid_user_id():
    # Проверяет, что нечисловой user_id в пути возвращает статус 422 (ошибка валидации FastAPI)
    response = client.get("/api/v1/photos/not_a_number")
    assert response.status_code == 422


def test_get_user_photos_response_schema():
    # Проверяет, что ответ содержит все обязательные поля схемы: Photo (id, owner_id, date, sizes)
    # и PhotoSize (type, url, width, height)
    with patch("app.api.v1.endpoints.photos.fetch_all_photos", new=AsyncMock(return_value=[MOCK_PHOTO])):
        response = client.get("/api/v1/photos/123")

    data = response.json()
    photo = data["photos"][0]
    assert "id" in photo
    assert "owner_id" in photo
    assert "date" in photo
    assert "sizes" in photo
    size = photo["sizes"][0]
    assert "type" in size
    assert "url" in size
    assert "width" in size
    assert "height" in size
