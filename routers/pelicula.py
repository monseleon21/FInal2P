from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException
from DB.conexion import Session
from models.peliculasDB import Pelicula
from modelsPydantic import modeloPelicula, modeloPeliculaResponse
from auth import verificar_token
from fastapi import Depends
from auth import verificar_token

routerPelicula = APIRouter()

#Endpoint consultar todos y en vez de usar el app lo cmabio por el nombre de royer Pelicula
@routerPelicula.get('/peliculas', response_model=list[modeloPeliculaResponse], tags=['ver todas'])
def obtener_p():
    db = Session()
    try:
        peliculas = db.query(Pelicula).all()
        return JSONResponse(content=jsonable_encoder(peliculas))
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'error al consultar todas las peliculas', 'exception': str(e)})
    finally:
        db.close()



#Endpoint consultar 1 Pelicula
@routerPelicula.get('/peliculas/{id}', response_model=modeloPeliculaResponse, tags=['Consultar 1 pelicula'])
def obtener_p(id: int):
    db = Session()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == id).first()
        if not pelicula:
            return JSONResponse(status_code=404, content={'message': 'No se encontro la Pelicula'})
        return JSONResponse(content=jsonable_encoder(pelicula))
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'error al buscar la pelicula', 'exception': str(e)})
    finally:
        db.close()


#Endpoint Agregar Pelicula
@routerPelicula.post('/peliculas', response_model=modeloPelicula, tags=['Guardar Pelicula'])
def agregar_p(pelicula: modeloPelicula):
    db = Session()
    try:
        nueva=Pelicula(**pelicula.model_dump())
        db.add(nueva)
        db.commit()
        return JSONResponse(status_code=202, content={'message':'Se agrego la Pelicula', 'pelicula': pelicula.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={'message': 'Error al agregar la pelicula', 'exception': str(e)})
    finally:
        db.close()


#Endpoint editar Pelicula
@routerPelicula.put('/peliculas/{id}', response_model=modeloPelicula, tags=['Editar'])
def editar_p(id: int, pelicula_actualizada: modeloPelicula):
    db = Session()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == id).first()
        if not pelicula:
            raise HTTPException(status_code=404, detail='Pelicula no encontrada')
        for campo, valor in pelicula_actualizada.model_dump().items():
            setattr(pelicula, campo, valor)
        db.commit()
        db.refresh(pelicula)
        return pelicula
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'Error al editar la pelicula', 'exception': str(e)})
    finally:
        db.close()


#Endpoint eliminar Pelicula
@routerPelicula.delete('/peliculas/{id}',dependencies=[Depends(verificar_token)],tags=['Eliminar peliculas'])
def eliminar_p(id: int):
    db = Session()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == id).first()
        if not pelicula:
            return JSONResponse(status_code=404, content={'message':'Pelicula no encontrada'})
        db.delete(pelicula)
        db.commit()
        return JSONResponse(content={'message':'Pelicula eliminada'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'Error al eliminar la pelicula', 'exception': str(e)})
    finally:
        db.close()