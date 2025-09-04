from fastapi import (
    FastAPI,
    Query,
    status,
    HTTPException,
    Path
)
from fastapi.responses import JSONResponse
# import uvicorn


app = FastAPI()

names_list = [
    {"id": 1, "name": "Ali"},
    {"id": 2, "name": "Hamed"},
    {"id": 3, "name": "Majid"},
    {"id": 4, "name": "Abbas"},
    {"id": 5, "name": "Mohsen"},
]

@app.get("/")
def index():
    return JSONResponse(
        content={"detail": "Hello World!"},
        status_code=status.HTTP_202_ACCEPTED
    )

# /names (GET(Retrieve), POST(Create))
@app.get("/names", status_code=status.HTTP_200_OK)
def retrieve_names_list(q: str | None = Query(default=None, max_length=20, alias="search")):
    if q:
        return [
            item for item in names_list if item["name"] == q
        ]
    return names_list

@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name:str):
    name_obj = {
        "id": names_list[-1]["id"] + 1,
        "name": name
    }
    names_list.append(name_obj)
    return {"result": name_obj}

# /names/:id (GET(Retrieve), PUT/PATCH(Update), DELETE)
@app.get("/names/{name_id}", status_code=status.HTTP_200_OK)
def retrieve_name_detail(
    name_id: int = Path(
        alias="object_id",
        title="object id",
        description="The id of the name in names_list"
        )
    ):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(
        detail="object not found",
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def update_name_detail(name_id:int, new_name:str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = new_name
            return {"item_updated": item}
    raise HTTPException(
        detail="object not found",
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.delete("/names/{name_id}")
def delete_name_detail(name_id:int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(
                content={"detail": "object removed successfully"},
                status_code=status.HTTP_204_NO_CONTENT
            )
    raise HTTPException(
        detail="object not found",
        status_code=status.HTTP_404_NOT_FOUND
    )
        
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
