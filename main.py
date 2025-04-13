from fastapi import FastAPI
from DB.conexion import engine, Base
from routers.pelicula import routerPelicula
from fastapi import Body
from jose import jwt

app = FastAPI(
    title="API Peliculas",
    description="María Monserrat Campuzano León"
)

Base.metadata.create_all(bind=engine)
@app.get('/', tags=['inicio'])
def home():
    return{'message': 'Bienvenido API Peliculas de Monserrat León'}
app.include_router(routerPelicula)

@app.post("/login", tags=["auth"])
def login(username: str = Body(...), password: str = Body(...)):
    if username == "Monchis" and password == "123456789":
        token = jwt.encode({"sub": username}, "miclavesupersecreta", algorithm="HS256")
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")