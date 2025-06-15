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

@router.get("*/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return {"status": "OK", "data": hotel}


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
async def update_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных",
    description="Хоть так, а хоть так")

async def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data,
            exclude_unset=True,
            id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
