from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Simulación de base de datos de usuarios
db_users = [
    {"username": "usuario1", "password": "contraseña1"},
    {"username": "usuario2", "password": "contraseña2"},
]

class User(BaseModel):
    username: str
    password: str

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = User(username=username, password=password)
    for db_user in db_users:
        if db_user["username"] == user.username and db_user["password"] == user.password:
            return templates.TemplateResponse("reserve_parking.html", {"request": request})
    raise HTTPException(status_code=401, detail="Credenciales inválidas")
