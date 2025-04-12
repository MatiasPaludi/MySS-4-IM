import queue 
"""libreria para manejar colas (Estructuras FIFO: First in, First Out)--> (el primero en entrar es el primero en salir).
Sus funciones basicas son:
 Función	|        ¿Qué hace?	           |         Ejemplo                          |
 -----------|------------------------------|------------------------------------------|
  put(x)	|    Mete x en la cola	       |    cola.put("Cliente A")                 |
  get()	    |  Saca el primer elemento	   |    cola.get() → "Cliente A"              |
 qsize()	|   Cantidad de elementos	   |    cola.qsize() → 2                      |
 empty()	|     ¿Está vacía?	           |    cola.empty() → True(si) o False(no)   |


""" 
import random
from tabulate import tabulate


def strftime_a_min(hora):  # "HH:MM:SS" -> minutos
    h, m, s = map(int, hora.split(":"))
    return h * 60 + m + s / 60

""" - hora.split(":") --> convierte de string "01:00:50" a rellenar un array con los valores de textos ["10":"40":"30"]
    - map(int,....) --> convierte la lista de strings a enteros [1,30,45]
    - y luego asigna a (h,m,s) --> h=1 m=30 s=45
luego de asignarse return -> (h*60) = minutos ;(s/60) = minutos.  es decir que retorna la conversion de la hora en minutos. 
"""




def min_a_strftime(tiempo):  # minutos -> "HH:MM:SS"
    if tiempo == float('inf'):
        return "----"
    horas = int(tiempo) // 60  # tiempo a horas
    minutos = int(tiempo) % 60 # minutos restantes (%) modulo da el resto despues de dividir
    segundos = int((tiempo * 60) % 60) # segundos restantes  --> tiempo * 60 a segundos y luego lo mismo de arriba. 
   
    horas_strftime = str(horas).zfill(2)
    minutos_strftime = str(minutos).zfill(2)
    segundos_strftime = str(segundos).zfill(2)
   
   #cadena para unir el horario de la forma HH:MM:SS

    hora_fstr = horas_strftime +":"+minutos_strftime+":"+segundos_strftime
   
    return hora_fstr

""" Convierte un número decimal de minutos de vuelta a formato strings format time 
Si fin_servicio == inf, siempre se ejecuta la llegada primero. por ende no se debe calcular un fin de servicio, y devuelve "----"

 return hota_fstr --> Esta línea devuelve la cadena con formato "HH:MM:SS", y .zfill(2) asegura que cada número tenga dos dígitos,
                                     agregando ceros si hace falta.

 ---> zfill(2) rellena con ceros a la izquierda para asegurarse de que el string tenga al menos 2 caracteres.
 """

def valor_aleatorio(distrib, minimo, maximo):
    if distrib == "uniforme":
        return random.uniform(minimo, maximo)
    elif distrib == "exponencial":
        return random.expovariate(1 / ((minimo + maximo) / 2))
    elif distrib == "normal":
        return random.gauss((minimo + maximo) / 2, (maximo - minimo) / 6)
    return (minimo + maximo) / 2

""" def valor_aleatorio(distrib, minimo, maximo)  -->  distrib => (uniforme,exponencial,normal)
                                                       minimo => (valor minimo del rango)
                                                       maximo => (valor maximo del rango)

uniforme --> cualquier valor aleatorio tiene la misma probabilidad de salir dentro del rango.

exponencial --> lambda representa la tasa de ocurrencia en la funcion random.expovariate(λ), λ = 1/media y la media es (min+MAX)/2
                por ello λ = [1/((min+MAX)/2)] --- EJEMP: λ = 0.0167= 1,67/100, nos dara un valor bajo entre los rangos ya que la exponencial
                cae rapido y nos dice que la probabilidad de evento es 1,67 cada 100 minutos.

random.gauss(media, desviacion_estandar) --> media = (minimo + maximo) / 2
                                             desviacion = (maximo - minimo) / 6
    EJEMPLO:  
    media = (20 + 40) / 2 = 30           |  random.gauss(30, 3.33) --> (29.8, 30.2, 33.0, 27.5, 35.4, 24.9, 40.1...)
    desviacion = (40 - 20) / 6 = 3.33    |        
"""
def simular():
    # pido rangos de simulacion por teclado y utilizo la funcion para convertir a minutos los valores strings, para facilitar calculos
    hora_ini = strftime_a_min(input("Hora de inicio (HH:MM:SS): "))
    hora_fin = strftime_a_min(input("Hora de fin (HH:MM:SS): "))

#  ----  Defino si las llegadas son aleatorias o constantes lo mismo con el tiempo de servicio.-----
# (a) --> defino el tipo de ditribucion asignando string a dist_llegada. y los valores de rangos min_lleg y max_lleg
# != a --> defino el valor constante asignandolo a la variable const_lleg.
    tipo_llegada = input("¿Hora de llegada de cliente aleatoria o constante? (a/c): ").lower()
    if tipo_llegada == "a":
        dist_llegada = input("Distribución (uniforme, exponencial, normal): ").lower()
        min_lleg, max_lleg = map(int, input("Mín y máx en segundos (ej: 20 40): ").split())
    else:
        const_lleg = int(input("Hora de llegada de cliente constante (segundos): "))

    tipo_servicio = input("¿Tiempo de servicio aleatorio o constante? (a/c): ").lower()
    if tipo_servicio == "a":
        dist_serv = input("Distribución (uniforme, exponencial, normal): ").lower()
        min_serv, max_serv = map(int, input("Mín y máx en segundos (ej: 40 60): ").split())
    else:
        const_serv = int(input("Tiempo de servicio constante (segundos): "))

# ---- ESTADO INICIAL DEL SISTEMA -----

    en_cola = int(input("Clientes inicialmente en cola: "))
    ps_ocupado = int(input("¿Puesto de servicio ocupado al inicio? (1=sí, 0=no): "))
    llegada_inicial = strftime_a_min(input("Hora inicial de próxima llegada (HH:MM:SS): "))
    fin_servicio_inicial = float('inf')
    if ps_ocupado:
        fin_servicio_inicial = strftime_a_min(input("Hora inicial de próximo fin de servicio (HH:MM:SS): "))

    # Inicialización de variables 
    tiempo  = hora_ini
    llegada = llegada_inicial
    fin_servicio = fin_servicio_inicial
    cola = queue.Queue()
    #cola = queue.Queue()  --> crea la cola 
#for i in range(en_cola):  ---> crea la cola de clientes iniciales, si hay por ejemplo 3 clientes en cola al iniciar la simulacion
#cola.put(i + 1)       ---> entonces (en_cola=3) por ello el for generara cola.put(1), cola.put(2), cola.put(3)
 #                          de la forma que range(3) -> [0,1,2] entonces cola.put(i=0 + 1 ) = cola.put(1) y asi hasta llegar al rango

 ## carga los clientes a la cola si es que hay antes de iniciar la simulacion.
    for i in range(en_cola):
        cola.put(i + 1)

# verifico si hay un cliente en PS o no. y contabilizo con total clientes si es que cuantos hay en el sistema. 
    cliente_actual = 0 if ps_ocupado else None 
    # ps=0 -> none (no hay cliente en servicio)  ps=1 -> 0 (si hay cliente en serv)
    atendidos = 0
    total_clientes = en_cola + (1 if ps_ocupado else 0)

# Forma de la Tabla 
    tabla = []
    columnas = ["Hora Actual", "H Próx.LLC", "H Próx.FS", 
                "Cola", "PS", "C_At"]

    # Agrega estado inicial --> guardamos el estado de inicio de simulacion, es decir, primera fila de la tabla.
    tabla.append([
        min_a_strftime(tiempo),
        min_a_strftime(llegada),
        min_a_strftime(fin_servicio),
        cola.qsize(),
        1 if cliente_actual else 0,
        atendidos
    ])
    # simulación 
    while tiempo <= hora_fin:
        if llegada <= fin_servicio:
            tiempo = llegada
            if tiempo > hora_fin:
                tabla.append([
                    min_a_strftime(tiempo),
                    min_a_strftime(llegada),
                    min_a_strftime(fin_servicio),
                    cola.qsize(),
                    1 if cliente_actual else 0,
                    atendidos
                    ])
                break
    
            total_clientes += 1
            cola.put(total_clientes)
            if tipo_llegada == "a":
                llegada += valor_aleatorio(dist_llegada, min_lleg / 60, max_lleg / 60)
            else:
                llegada += const_lleg / 60

            if cliente_actual is None and not cola.empty():
                cliente_actual = cola.get()
                if tipo_servicio == "a":
                    fin_servicio = tiempo + valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                else:
                    fin_servicio = tiempo + const_serv / 60

        #cuando la hora de llegada cliente es mayor a fin de servicio..
        
        else:
            tiempo = fin_servicio
            if tiempo > hora_fin:
                tabla.append([
                    min_a_strftime(tiempo),
                    min_a_strftime(llegada),
                    min_a_strftime(fin_servicio),
                    cola.qsize(),
                    1 if cliente_actual else 0,
                    atendidos
                    ])
                break
            atendidos += 1
            cliente_actual = None  #libera el puesto de servicio
            if not cola.empty():
                cliente_actual = cola.get() #toma el siguiente cliente si es que la cola no esta vacia
                if tipo_servicio == "a":  # nuevo fin de servicio
                    fin_servicio = tiempo + valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                else:
                    fin_servicio = tiempo + const_serv / 60
            else:   #si no hay cola, se asigna un valor infinito que es menor a cualquier llegada. 
                fin_servicio = float('inf')

#guardo el estado del sistema al final de cada iteración para guardar el estado del sistema y mostrarlo en la tabla.

        tabla.append([
            min_a_strftime(tiempo),
            min_a_strftime(llegada),
            min_a_strftime(fin_servicio),
            cola.qsize(),
            1 if cliente_actual else 0,  #Si hay alguien → 1 if cliente_actual es verdadero, devuelve 1.

                                         #Si no hay nadie (cliente_actual = None) → devuelve 0.
            atendidos
        ])

    print(tabulate(tabla, headers=columnas, tablefmt="fancy_grid", stralign="center"))

     # Mostrar información de la última iteración
    ultima_iteracion = len(tabla)
    ultima_fila = tabla[-1]
    print(f"\nÚltima iteración (número {ultima_iteracion}):")
    for nombre_col, valor in zip(columnas, ultima_fila):
        print(f"{nombre_col}: {valor}")

simular()


# Evita que la ventana se cierre al ejecutarlo como .exe
input("\nPresione Enter para salir...")
