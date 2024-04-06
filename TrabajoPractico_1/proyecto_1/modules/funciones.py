from random import choice
import matplotlib.pyplot as plt
from collections import defaultdict

def agregar_pelicula_lista(lista,frase,peli):
    #crea un diccionario con los datos de las peliculas y sus frases
    pelicula={
        'peli':peli,
        'frase':frase,
    }
    lista.append(pelicula)

def peliculas_sin_repetir(peli, solo_pelis):
    #crea una lista solo de peliculas
    solo_pelis.append(peli)


def leer_archivo(archivo,lista,solo_pelis):
    '''se encarga de leer el archivo con los datos de las frases con sus peliculas
     y los guarda en un diccionario y una lista para las peliculas, mediante las dos funciones anteriores'''
    with open(archivo, 'r',encoding="utf-8") as archi:
        for linea in archi:
            pelicula=linea.rstrip().split(";")
            agregar_pelicula_lista(lista,pelicula[0],pelicula[1])
            peliculas_sin_repetir(pelicula[1],solo_pelis)

def iniciar_trivia(lista_fyp,pelis_sin_rep,opciones,correct):
    #crea las opciones de una frase y tres peliculas e indica la correcta 
    p1=choice(lista_fyp)
    lista_fyp.remove(p1)
    for pel in pelis_sin_rep:
        if pel==p1['peli']:
            pelis_sin_rep.remove(p1['peli'])
    p2=choice(pelis_sin_rep)
    pelis_sin_rep.remove(p2)
    p3=choice(pelis_sin_rep)
    pelis_sin_rep.append(p2)
    correct.extend([p1['frase'],p1['peli']])
    opciones.extend([p1['peli'],p2,p3])
    
    

def opcion_random(opciones):
    #ordena de manera aleatoria las tres opciones
    p1=choice(opciones)
    opciones.remove(p1)
    p2=choice(opciones)
    opciones.remove(p2)
    p3=opciones[0]
    opciones.extend([p1,p2,p3])
    

def guardar_partida(archi_usuarios,usuario_n,op_cor,op_ele,fecha):
    #guarda la partida en el archivo indicado
    with open(archi_usuarios, 'a') as archi:
        archi.write(f"{usuario_n},{op_cor},{op_ele},{fecha}\n")


def leer_usuarios(archivo_usuarios,lista_usuarios):
    #lee el archivo de usuario y lo guarda en una lista
    with open(archivo_usuarios, 'r') as archi:
        for line in archi:
            user=line.rstrip().rsplit(',')
            lista_usuarios.append(user)

def generar_graficas(lista_usuarios):
    #genera las dos graficas con los datos proporcionados y los guarda como pdf y png
    partidas_por_fecha = defaultdict(lambda: {
        "aciertos": 0, 
        "desaciertos": 0,
    })
    for line in lista_usuarios:
        fecha=line[3]
        partidas_por_fecha[fecha]["aciertos"]+=int(line[1])
        partidas_por_fecha[fecha]["desaciertos"]+=int(line[2])-int(line[1])

    fechas = list(partidas_por_fecha.keys())
    fechas.sort()
    aciertos_acumulados = [partidas_por_fecha[fecha]["aciertos"] for fecha in fechas]
    desaciertos_acumulados = [partidas_por_fecha[fecha]["desaciertos"] for fecha in fechas]
    aciertos_totales = sum(aciertos_acumulados)
    desaciertos_totales = sum(desaciertos_acumulados)
    
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, aciertos_acumulados, label="Aciertos")
    plt.plot(fechas, desaciertos_acumulados, label="Desaciertos")
    plt.xlabel("Fechas de juego")
    plt.ylabel("Cantidad")
    plt.title("Aciertos y desaciertos acumulados")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("./static/grafica_acumulados.pdf")
    plt.savefig("./static/grafica_acumulados.png")

    plt.figure(figsize=(6, 6))
    labels = 'Aciertos', 'Desaciertos'
    sizes = [aciertos_totales, desaciertos_totales]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    plt.title('Porcentaje de aciertos y desaciertos acumulados')
    plt.axis('equal')

    plt.savefig("./static/grafica_porcentajes.pdf")
    plt.savefig("./static/grafica_porcentajes.png")
