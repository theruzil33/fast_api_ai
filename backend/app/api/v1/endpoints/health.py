from fastapi import APIRouter

router = APIRouter()


@router.get("/hello", summary="Hello World")
async def hello_world():
    return {"message": "Hello, World!"}
