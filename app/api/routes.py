from fastapi import APIRouter

from app.service import process_search

router = APIRouter()

@router.get("/api/v1/search")
async def search( search_string:str):
    result = await process_search(
        search_string
    )
    return result