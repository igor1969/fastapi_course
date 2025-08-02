from fastapi import APIRouter, Body, Path
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotels_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotels_id=hotels_id)


@router.get("/{hotel_id}/rooms/room_id")
async def get_room(hotels_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotels_id=hotels_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotels_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Double Suite в Red Square",
        "value": {
            "title": "Double Suite",
            "description": "Уютный номер с балконом",
            "price": 4500,
            "quantity": 2,
            "hotels_id": 1
        }
    },
    "2": {
        "summary": "Single Sea View в Burja Haliff",
        "value": {
            "title": "Single Sea View",
            "description": "Окно в море, только для одного",
            "price": 5500,
            "quantity": 1,
            "hotels_id": 2
        }
    },
})):
    _room_data = RoomAdd(hotels_id=hotels_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotels_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotels_id=hotels_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotels_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            _room_data,
            exclude_unset=True,
            id=room_id,
            hotels_id=hotel_id
        )
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotels_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotels_id)
        await session.commit()
    return {"status": "OK"}