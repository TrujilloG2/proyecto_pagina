from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)

app.secret_key ='1234'
mybase = mysql.connector.connect (
    host = 'localhost', user = 'root', password = 'tg280701', database = 'pagina'
)
@app.route('/templates/inicio.html') 
def inicio():
    if 'nombre' in session:
        return render_template('/inicio.html',nombre = session['nombre'])
    else: 
        return redirect(url_for('login'))
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['correo']
        contra = request.form['password']
        repite_contra = request.form['password2']
        if contra== repite_contra:
            mycursor = mybase.cursor()
            mycursor.execute("SELECT * FROM login WHERE usuario = %s", (email,))
            resultado = mycursor.fetchone()
            if resultado:
                # El registro ya existe, enviar un mensaje y redirigir al usuario
                return render_template('/registro.html', mensaje = 'El registro ya existe!')
            else:
                mycursor.execute("INSERT INTO login (usuario, password) VALUES (%s, %s)", (email, contra))
                mybase.commit()
                return render_template('/registro.html', mensaje = 'Cuenta creada con exito!')
        else:
            return render_template('/registro.html', mensaje = 'Las contraseñas no coinciden :(')
    else:
        return render_template('/registro.html')
@app.route('/')
def home():
    return render_template('/index.html')
@app.route('/templates/login.html', methods = ['GET', 'POST'])

def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        mycursor = mybase.cursor()
        mycursor.execute("select * from login where usuario = %s and password = %s", (correo, password))
        nombre = mycursor.fetchone()
        if nombre:
            session['nombre'] = nombre[1] 
            return redirect(url_for ('inicio'))
        else: 
            return render_template('/login.html', aviso = 'correo y contraseña incorretos')
    else:  
        return render_template('/login.html')
@app.route('/logout')
def logout(): 
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0') 



