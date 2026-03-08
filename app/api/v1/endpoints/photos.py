from fastapi import APIRouter, HTTPException

from app.schemas.photos import Photo, PhotosResponse
from app.services.vk import fetch_all_photos

router = APIRouter()


@router.get("/{user_id}", response_model=PhotosResponse, summary="Получить все фото пользователя VK")
async def get_user_photos(user_id: int):
    try:
        items = await fetch_all_photos(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"VK API недоступен: {e}")

    photos = [Photo(**item) for item in items]

    return PhotosResponse(
        user_id=user_id,
        total=len(photos),
        photos=photos,
    )
