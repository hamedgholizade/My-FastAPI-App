from fastapi import FastAPI
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
    return {
        "message": "Hello World!"
        }

# /names (GET(Retrieve), POST(Create))
@app.get("/names")
def retrieve_names_list():
    return names_list

@app.post("/names")
def create_name(name:str):
    name_obj = {
        "id": names_list[-1]["id"] + 1,
        "name": name
    }
    names_list.append(name_obj)
    return {"result": name_obj}

# /names/:id (GET(Retrieve), PUT/PATCH(Update), DELETE)
@app.get("/names/{name_id}")
def retrieve_name_detail(name_id:int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    return {"detail": "object not found"}

@app.put("/names/{name_id}")
def update_name_detail(name_id:int, new_name:str):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = new_name
            return {"item_updated": item}
    return {"detail": "object not found"}

@app.delete("/names/{name_id}")
def delete_name_detail(name_id:int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"detail": "object removed successfully"}
    return {"detail": "object not found"}
        
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
