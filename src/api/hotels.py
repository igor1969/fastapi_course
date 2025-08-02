from fastapi import Query, APIRouter, Body


from src.api.dependencies import PaginationDep, DBDep

from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Title"),
        location: str | None = Query(None, description="City"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router.get("*/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.post("")
async def create_hotel(db: DBDep, hotel_data: Hotel = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: Hotel):

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных",
    description="Хоть так, а хоть так")

async def partial_update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH
):
    await db.hotels.edit(
        hotel_data,
        exclude_unset=True,
        id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel( db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
