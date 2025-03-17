from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {
        "id": 1,
        "title": "Sochi",
        "name": "sochi"
     },
    {
        "id": 2,
        "title": "Dubai",
        "name": "dubai"
    },
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="ID"),
    title: str | None = Query(None, description="City")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "Updated"}
    return {"status": "Hotel not found"}


from fastapi import Body

@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    data: dict = Body(...)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            # Обновляем только те поля, которые пришли
            for key in data:
                if key in hotel:  # Меняем только если такое поле есть у отеля
                    hotel[key] = data[key]
            return {"status": "Partially Updated"}
    return {"status": "Hotel not found"}

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"]  != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


