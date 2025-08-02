from fastapi import APIRouter, Body, Path

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotels_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotels_id=hotels_id)


@router.get("/{hotel_id}/rooms/room_id")
async def get_room(hotels_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotels_id=hotels_id)


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotels_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotels_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotels_id=hotels_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep
):
    _room_data = RoomPatch(hotels_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotels_id=hotel_id
    )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotels_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotels_id)
    await db.commit()
    return {"status": "OK"}