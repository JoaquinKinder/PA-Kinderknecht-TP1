from flask import render_template, redirect, url_for, request
import datetime
from modules.config import app
from modules.funciones import leer_archivo,iniciar_trivia,opcion_random,guardar_partida,leer_usuarios,generar_graficas

archivo ="./data/frases_de_peliculas.txt"
archivo_user="./data/usuarios.txt"
frases_y_pelis=[]
pelis_sin_rep=[]
num_p=int(0)
total_num=0
usuario=''
elegida=''
correcta=[]
lista_usuarios=[]
aciertos=0
fecha=""
leer_archivo(archivo,frases_y_pelis,pelis_sin_rep)
pelis_sin_rep=set(pelis_sin_rep)
pelis_sin_rep=list(pelis_sin_rep)
pelis_sin_rep.sort()


@app.route("/",  methods=["GET", "POST"])
def inicio():
    global aciertos
    aciertos=0
    return render_template("inicio.html")


@app.route("/trivia", methods=["GET", "POST"])
def trivia():
    global num_p
    global usuario
    global total_num
    global fecha
    if num_p==0:
        if request.method == "POST":
            num_p=request.form['input_num_preguntas']
            num_p=int(num_p)
            usuario=request.form['input_usuario']
            total_num=num_p
            fecha=datetime.datetime.now()
            fecha=fecha.strftime("%Y/%m/%d %H:%M")
    global correcta
    correcta=[]
    opciones=[]
    iniciar_trivia(frases_y_pelis,pelis_sin_rep,opciones,correcta)
    opcion_random(opciones)
    return render_template("trivia.html",opciones=opciones,correcta=correcta)

@app.route("/respuesta", methods=["GET", "POST"])
def respuesta():
    global aciertos
    global num_p
    global fecha
    global total_num
    if request.method =="POST":
        elegida=request.form['opcion']
    resp=''
    if correcta[1] == elegida:
        resp='correcta, Felicitaciones'
        aciertos=aciertos+1
    else:
        resp='Incorrecta '
    num_p=num_p-1
    if num_p==0:
        guardar_partida(archivo_user,usuario,aciertos,total_num,fecha)
    return render_template("respuesta.html",resp=resp,correcta=correcta,aciertos=aciertos,num_p=num_p,total_num=total_num)
    
    
@app.route("/puntuaciones", methods=["GET", "POST"])
def puntuaciones():
    lista_usuarios=[]
    leer_usuarios(archivo_user,lista_usuarios)
    generar_graficas(lista_usuarios)
    return render_template("puntuaciones.html",lista_usuarios=lista_usuarios)

@app.route("/peliculas", methods=["GET", "POST"])
def ver_peliculas():
    pelis_sin_rep.sort()
    return render_template("peliculas.html",pelis_sin_r=pelis_sin_rep)

@app.route("/graficas", methods=["GET", "POST"])
def graficas():
    return render_template("graficas.html")

if __name__=="__main__":
    app.run()
