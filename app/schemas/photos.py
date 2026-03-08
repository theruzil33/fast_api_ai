from pydantic import BaseModel


class PhotoSize(BaseModel):
    type: str
    url: str
    width: int
    height: int


class Photo(BaseModel):
    id: int
    owner_id: int
    date: int
    sizes: list[PhotoSize]
    text: str = ""


class PhotosResponse(BaseModel):
    user_id: int
    total: int
    photos: list[Photo]
