from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL base de tu API FastAPI
API_URL = 'http://127.0.0.1:8000/peliculas'

@app.route('/')
def index():
    response = requests.get(API_URL)
    peliculas = response.json()
    return render_template('index.html', peliculas=peliculas)



@app.route('/agregar', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos = {
            "titulo": request.form['titulo'],
            "genero": request.form['genero'],
            "anio": int(request.form['anio']),
            "clasificacion": request.form['clasificacion']
        }
        requests.post(API_URL, json=datos)
        return redirect(url_for('index'))
    return render_template('agregar.html')


@app.route('/detalle/<int:id>')
def detalle(id):
    response = requests.get(f'{API_URL}/{id}')
    pelicula = response.json()
    return render_template('detalles.html', pelicula=pelicula)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        datos = {
            "titulo": request.form['titulo'],
            "genero": request.form['genero'],
            "anio": int(request.form['anio']),
            "clasificacion": request.form['clasificacion']
        }
        requests.put(f'{API_URL}/{id}', json=datos)
        return redirect(url_for('index'))
    else:
        pelicula = requests.get(f'{API_URL}/{id}').json()
        return render_template('editar.html', pelicula=pelicula)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    requests.delete(f'{API_URL}/{id}')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
