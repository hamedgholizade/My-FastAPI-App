from typing import List
from fastapi import (
    FastAPI,
    Query,
    status,
    HTTPException,
    Path,
    File,
    UploadFile,
    Depends
)
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
# import uvicorn

from schemas import (
    PersonCreateSchema,
    PersonUpdateSchema,
    PersonResponseSchema
)
from database import (
    Base,
    engine,
    get_db,
    Person
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up")
    Base.metadata.create_all(bind=engine)
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
@app.get(
    "/names",
    status_code=status.HTTP_200_OK,
    response_model=List[PersonResponseSchema]
    )
def retrieve_names_list(
    q: str | None = Query(default=None,max_length=20,alias="search"),
    db: Session = Depends(get_db)
    ):
    query = db.query(Person)
    if q:
        query = query.filter_by(name=q)
    result = query.all()
    return result

@app.post(
    "/names",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonResponseSchema
    )
def create_name(
    requset: PersonCreateSchema,
    db: Session = Depends(get_db)
    ):
    new_person = Person(name=requset.name)
    db.add(new_person)
    db.commit()
    return new_person

# /names/:id (GET(Retrieve), PUT/PATCH(Update), DELETE)
@app.get(
    "/names/{name_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonResponseSchema
    )
def retrieve_name_detail(
    name_id: int = Path(
        title="object id",
        description="The id of the name"
        ),
    db: Session = Depends(get_db)
    ):
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        return person
    raise HTTPException(
        detail="object not found",
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.put(
    "/names/{name_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonResponseSchema
    )
def update_name_detail(
    request: PersonUpdateSchema,
    name_id: int = Path(),
    db: Session = Depends(get_db)
    ):
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        person.name = request.name
        db.commit()
        db.refresh(person)
        return person
    raise HTTPException(
        detail="object not found",
        status_code=status.HTTP_404_NOT_FOUND
    )

@app.delete("/names/{name_id}")
def delete_name_detail(name_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
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
