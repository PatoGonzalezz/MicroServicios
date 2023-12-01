from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Base de datos simulada de espacios de estacionamiento
parking_spaces = {
    1: {"id": 1, "name": "Espacio 1", "available": True},
    2: {"id": 2, "name": "Espacio 2", "available": True},
    # Agrega más espacios de estacionamiento aquí según sea necesario
}

class ParkingReservation(BaseModel):
    space_id: int
    user_id: int

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("reserve_parking.html", {"request": request})

@app.get("/parking-spaces")
async def get_parking_spaces():
    return parking_spaces

@app.post("/reserve-parking", status_code=201)
async def reserve_parking(reservation: ParkingReservation):
    space_id = reservation.space_id
    if space_id not in parking_spaces:
        raise HTTPException(status_code=404, detail="Espacio de estacionamiento no encontrado")
    
    if not parking_spaces[space_id]["available"]:
        raise HTTPException(status_code=400, detail="Espacio de estacionamiento no disponible")
    
    parking_spaces[space_id]["available"] = False
    return {"message": f"Espacio de estacionamiento {space_id} reservado por el usuario {reservation.user_id}"}
