import httpx
import pytest
import respx

from app.services.vk import fetch_all_photos

VK_URL = "https://api.vk.com/method/photos.getAll"

PHOTO = {
    "id": 1,
    "owner_id": 123,
    "date": 1700000000,
    "text": "",
    "sizes": [{"type": "x", "url": "https://example.com/photo.jpg", "width": 604, "height": 453}],
}


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_photos_success():
    # Проверяет, что при одной странице результатов возвращается список с правильным количеством фото
    respx.get(VK_URL).mock(return_value=httpx.Response(
        200, json={"response": {"count": 1, "items": [PHOTO]}}
    ))

    result = await fetch_all_photos(123)

    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["owner_id"] == 123


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_photos_empty():
    # Проверяет, что при отсутствии фото у пользователя возвращается пустой список
    respx.get(VK_URL).mock(return_value=httpx.Response(
        200, json={"response": {"count": 0, "items": []}}
    ))

    result = await fetch_all_photos(123)

    assert result == []


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_photos_pagination():
    # Проверяет пагинацию: при count=3 и batch_size=200 делается 2 запроса,
    # итого возвращаются все 3 фото
    page1 = [{"id": i, "owner_id": 123, "date": 0, "text": "", "sizes": []} for i in range(1, 3)]
    page2 = [{"id": 3, "owner_id": 123, "date": 0, "text": "", "sizes": []}]

    route = respx.get(VK_URL)
    route.side_effect = [
        httpx.Response(200, json={"response": {"count": 3, "items": page1}}),
        httpx.Response(200, json={"response": {"count": 3, "items": page2}}),
    ]

    result = await fetch_all_photos(123)

    assert len(result) == 3
    assert route.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_photos_vk_error():
    # Проверяет, что ошибка в теле ответа VK API (поле "error") выбрасывает ValueError
    # с кодом и текстом ошибки
    respx.get(VK_URL).mock(return_value=httpx.Response(
        200, json={"error": {"error_code": 15, "error_msg": "Access denied"}}
    ))

    with pytest.raises(ValueError, match="VK API error 15: Access denied"):
        await fetch_all_photos(123)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_photos_http_error():
    # Проверяет, что HTTP-ошибка (статус 500) выбрасывает исключение httpx.HTTPStatusError
    respx.get(VK_URL).mock(return_value=httpx.Response(500))

    with pytest.raises(httpx.HTTPStatusError):
        await fetch_all_photos(123)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_photos_passes_correct_params():
    # Проверяет, что в запрос передаются правильные параметры: owner_id, photo_sizes, no_service_albums
    route = respx.get(VK_URL).mock(return_value=httpx.Response(
        200, json={"response": {"count": 0, "items": []}}
    ))

    await fetch_all_photos(456)

    request = route.calls[0].request
    assert b"owner_id=456" in request.url.query
    assert b"photo_sizes=1" in request.url.query
    assert b"no_service_albums=0" in request.url.query
