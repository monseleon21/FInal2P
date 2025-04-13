from pydantic import BaseModel, Field

class modeloPelicula(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=100)
    genero: str = Field(..., min_length=4, max_length=50)
    anio: int = Field(..., ge=1000, le=9999)
    clasificacion: str = Field(..., min_length=1, max_length=1, pattern="^[ABC]$")

class modeloPeliculaResponse(modeloPelicula):
    id: int

    class Config:
        orm_mode = True
