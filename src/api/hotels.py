from compileall import compile_path

from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository

from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Hotels"])



@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Title"),
        location: str | None = Query(None, description="City"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Sochi",
        "value": {
            "title": "Hotel Red Square Sochi 1 line",
            "location": "Sochi, Kotoff str,25"
        }
    },
    "2": {
        "summary": "Dubai",
        "value": {
            "title": "Hotel Burja Haliff 1 line",
            "location": "Dubai, Rahulla, 35"
        }
    },

})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["hotel_id"] == hotel_id:
            hotel["title"] = hotel_data.title,
            hotel["name"] = hotel_data.name
            return {"status": "Updated"}
    return {"status": "Hotel not found"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных",
    description="Хоть так, а хоть так")

def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"status": "Partially Updated"}
    return {"status": "Hotel not found"}

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"]  != hotel_id]
    return {"status": "OK"}
