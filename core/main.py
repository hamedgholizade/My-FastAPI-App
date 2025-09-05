from typing import List
from fastapi import (
    FastAPI,
    Query,
    status,
    HTTPException,
    Path,
    Form,
    Body,
    File,
    UploadFile,
)
from dataclasses import dataclass
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
# import uvicorn


names_list = [
    {"id": 1, "name": "Ali"},
    {"id": 2, "name": "Hamed"},
    {"id": 3, "name": "Majid"},
    {"id": 4, "name": "Abbas"},
    {"id": 5, "name": "Mohsen"},
]

# Events of FastAPI
# @app.on_event("startup")
# async def startup_event():
#     print("starting the application")

# @app.on_event("shutdown")
# async def shutdown_event():
#     print("shutting down the application")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up")
    yield
    print("Application shutting down")


app = FastAPI(lifespan=lifespan)

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

@dataclass
class Student:
    name: str
    age: int | None = None
    
@dataclass
class StudentResponse:
    id: int
    name: str

@app.post(
    "/names",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentResponse
    )
def create_name(student: Student):
    name_obj = {
        "id": names_list[-1]["id"] + 1,
        "name": student.name
    }
    names_list.append(name_obj)
    return name_obj

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
def update_name_detail(name_id: int = Path(), new_name: str = Form()):
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
    
# Upload-File-ByFile
@app.post("/send_file")
async def send_file(file: bytes = File(...)):
    print(file)
    return {
        "file_size": len(file)
    }

# Upload-File-ByUpLoadFile
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    print(file.__dict__)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content)
    }

@app.post("/upload_multiple")
async def upload_multiple(files: List[UploadFile]):
    return [
        {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": len(await file.read())
        }
        for file in files
    ]
        
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
