from fastapi import APIRouter, Depends, Query, status, HTTPException
from db import db_dependency

router = APIRouter(
    prefix="/video",
    tags=["video"]
)


@router.get("/video-search")
async def search_video(query: str = Query(None, description="Search query for title and description")):
    search_query = {
        "$and": [{'visibility': 'public'}]  # Ensure that only public videos are searched
    }

    if query:
        search_query["$and"].append({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        })
    else:
        raise HTTPException(status_code=400, detail="No search query provided")
    
    results = db_dependency.videos.find(search_query)

    # Serialize the results
    serialized_results = [
        {
            "id": str(result["_id"]),
            "title": result["title"],
            "description": result["description"],
            "channel_id": result["channel_id"],
            "owner_id": result["owner_id"],
            "visibility": result["visibility"]
        } for result in results
    ]

    return serialized_results
