from fastapi import Query, APIRouter


from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        id: int | None = Query(None, description="ID"),
        title: str | None = Query(None, description="City"),
        page: int = Query(1, ge=1, description="Номер страницы"),
        per_page: int = Query(10, gt=0, description="Количество элементов на странице")
):
    # Фильтрация отелей по параметрам
    filtered_hotels = []
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue
        if title is not None and hotel["title"] != title:
            continue
        filtered_hotels.append(hotel)

    # Расчет индексов для пагинации
    start = (page - 1) * per_page
    end = start + per_page

    return filtered_hotels[start:end]


@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


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
