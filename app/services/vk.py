import httpx

from app.core.config import settings

VK_API_BASE = "https://api.vk.com/method"


async def fetch_all_photos(user_id: int, limit: int | None = None) -> list[dict]:
    """Выкачивает фотографии пользователя через photos.getAll с пагинацией.

    Args:
        user_id: ID пользователя VK.
        limit: максимальное количество фото. None — выгрузить все.
    """
    photos = []
    offset = 0
    batch = 200  # максимум на один запрос

    async with httpx.AsyncClient() as client:
        while True:
            count = batch if limit is None else min(batch, limit - len(photos))

            response = await client.get(
                f"{VK_API_BASE}/photos.getAll",
                params={
                    "owner_id": user_id,
                    "count": count,
                    "offset": offset,
                    "photo_sizes": 1,
                    "no_service_albums": 0,
                    "access_token": settings.VK_ACCESS_TOKEN,
                    "v": settings.VK_API_VERSION,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                error = data["error"]
                raise ValueError(f"VK API error {error['error_code']}: {error['error_msg']}")

            items = data["response"]["items"]
            photos.extend(items)

            if len(photos) >= data["response"]["count"] or not items:
                break
            if limit is not None and len(photos) >= limit:
                break

            offset += batch

    return photos
