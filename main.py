from fastapi import FastAPI
from DB.conexion import engine, Base
from routers.pelicula import routerPelicula

app = FastAPI(
    title="API Peliculas",
    description="María Monserrat Campuzano León"
)

Base.metadata.create_all(bind=engine)
@app.get('/', tags=['inicio'])
def home():
    return{'message': 'Bienvenido API Peliculas de Monserrat León'}
app.include_router(routerPelicula)