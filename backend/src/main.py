from fastapi import FastAPI, File, UploadFile
from typing import List
import os
import database
from fastapi.middleware.cors import CORSMiddleware
from models.user import User
from models.receta import Receta
from models.filtros import FiltroRecetas

app = FastAPI()

# Configura CORS para permitir solicitudes desde tu aplicación Vue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Reemplaza con la URL de tu frontend Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return ""

@app.post("/register/", response_model=str)
def register(user: User):
    return database.signup(user.email, user.password, user.userID)
    
@app.get("/receta/{name}")
def get_receta(name: str):
    print(database.get_recepta(name))

@app.get("/recetas/", response_model=tuple)
def get_recetas(filtro: FiltroRecetas):
    return database.get_receptes(filtro)

@app.post("/receta", response_model=str)
def publi_receta(receta: Receta, files: List[UploadFile] = File(...)):
    image_urls = []

    for file in files:
        # Lee el archivo en memoria
        image_data = file.file.read()

        # Sube la imagen a Firebase Storage y obtén la URL
        image_url = database.uploadImg(receta, image_data, file.filename)

        # Agrega la URL de la imagen a la lista de URLs
        image_urls.append(image_url)

        receta.images = image_urls

    database.create_recepta(receta)
    return "200"