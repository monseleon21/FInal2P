from pydantic import BaseModel, Field

class modeloPelicula(BaseModel):
    
    titulo:str = Field(..., min_length=2, max_length=100, description='Titulo de pelicula, minimo 2 caracteres')

    genero:str = Field(..., min_length=4, max_length=50, description='Genero de pelicula, minimo 4 caracteres')

    anio:int = Field(..., ge=1000, le=9999, description='Año de pelicula, 4 digitos')

    clasificacion:str = Field(..., min_length=1, max_length=1, patterns="^[ABC]$", description='Solo 1 caracter A, B, C')

    class modeloPeliculaResponse(modeloPelicula):
        id: int
        class Config:
            orm_mode=True