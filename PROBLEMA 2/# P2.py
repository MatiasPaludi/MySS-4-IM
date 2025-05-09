import queue
import random
from tabulate import tabulate

def strftime_a_min(hora):
    h, m, s = map(int, hora.split(":"))
    return h * 60 + m + s / 60

def min_a_strftime(tiempo):
    if tiempo == float('inf'):
        return "----"
    horas = int(tiempo) // 60
    minutos = int(tiempo) % 60
    segundos = int((tiempo * 60) % 60)
    return f"{str(horas).zfill(2)}:{str(minutos).zfill(2)}:{str(segundos).zfill(2)}"

def valor_aleatorio(distrib, minimo, maximo):
    if distrib == "uniforme":
        return random.uniform(minimo, maximo)
    if distrib == "exponencial":
        return random.expovariate(1 / ((minimo + maximo) / 2))
    if distrib == "normal":
        return random.gauss((minimo + maximo) / 2, (maximo - minimo) / 6)
    return (minimo + maximo) / 2

def simular():
    hora_ini = strftime_a_min(input("Hora de inicio (HH:MM:SS): "))
    hora_fin = strftime_a_min(input("Hora de fin (HH:MM:SS): "))

    tiempo_llegada = input("¿Hora de llegada de cliente aleatoria o constante? (a/c): ").lower()
    if tiempo_llegada == "a":
        dist_llegada = input("Distribución llegadas (uniforme, exponencial, normal): ").lower()
        min_lleg = int(input("Tiempo mínimo entre llegadas (segundos): "))
        max_lleg = int(input("Tiempo máximo entre llegadas (segundos): "))
    else:
        const_lleg = int(input("Intervalo constante de llegada (segundos): "))

    tiempo_servicio = input("¿Tiempo de servicio aleatorio o constante? (a/c): ").lower()
    if tiempo_servicio == "a":
        dist_serv = input("Distribución servicio (uniforme, exponencial, normal): ").lower()
        min_serv = int(input("Tiempo mínimo de servicio (segundos): "))
        max_serv = int(input("Tiempo máximo de servicio (segundos): "))
    else:
        const_serv = int(input("Tiempo constante de servicio (segundos): "))

    tiempo_trabajo = input("¿Tiempo de trabajo aleatorio o constante? (a/c): ").lower()
    if tiempo_trabajo == "a":
        dist_trabajo = input("Distribución TIEMPO DE TRABAJO del servidor (uniforme, exponencial, normal): ").lower()
        min_trab = int(input("Duración mínima de trabajo del servidor (segundos): "))
        max_trab = int(input("Duración máxima de trabajo del servidor (segundos): "))
    else:
        const_trabajo = int(input("Tiempo constante de trabajo del servidor (segundos): "))

    tiempo_descanso = input("¿Tiempo de descanso aleatorio o constante? (a/c): ").lower()
    if tiempo_descanso == "a":
        dist_descanso = input("Distribución TIEMPO DE DESCANSO del servidor (uniforme, exponencial, normal): ").lower()
        min_desc = int(input("Duración mínima de descanso del servidor (segundos): "))
        max_desc = int(input("Duración máxima de descanso del servidor (segundos): "))
    else:
        const_descanso = int(input("Tiempo constante de descanso del servidor (segundos): "))

    en_cola = int(input("Clientes inicialmente en cola: "))
    ps_ocupado = int(input("¿Puesto de servicio ocupado al inicio? (1=sí, 0=no): "))
    servidor_presente = int(input("¿Servidor presente al inicio? (1=sí, 0=no): "))

    llegada = strftime_a_min(input("Hora inicial de próxima llegada (HH:MM:SS): "))

    if ps_ocupado == 1:
        fin_servicio = strftime_a_min(input("Hora inicial de fin de servicio (HH:MM:SS): "))
        cliente_actual = 0
    else:
        fin_servicio = float('inf')
        cliente_actual = None

    tiempo = hora_ini
    cola = queue.Queue()
    for i in range(en_cola):
        cola.put(i + 1)

    total_clientes = en_cola
    if ps_ocupado == 1:
        total_clientes += 1

    atendidos = 0

    if servidor_presente == 1:
        llegada_servidor = tiempo
        if tiempo_trabajo == "a":
            salida_servidor = tiempo + valor_aleatorio(dist_trabajo, min_trab / 60, max_trab / 60)
        else:
            salida_servidor = tiempo + const_trabajo / 60
    else:
        if tiempo_descanso == "a":
            llegada_servidor = tiempo + valor_aleatorio(dist_descanso, min_desc / 60, max_desc / 60)
        else:
            llegada_servidor = tiempo + const_descanso / 60
        salida_servidor = float('inf')

    tabla = []
    columnas = ["Hora Actual", "H próx.LLC", "H próx. FS", "H próx LLPS", "H próx FPS", "Cola", "PS", "S", "C_At"]

    while tiempo <= hora_fin:
        tabla.append([
            min_a_strftime(tiempo),
            min_a_strftime(llegada),
            min_a_strftime(fin_servicio),
            min_a_strftime(llegada_servidor),
            min_a_strftime(salida_servidor),
            cola.qsize(),
            1 if cliente_actual is not None else 0,
            servidor_presente,
            atendidos
        ])

        proximo_evento = min(llegada, fin_servicio, llegada_servidor, salida_servidor)
        tiempo = proximo_evento
        if tiempo > hora_fin:
            break

        if tiempo == llegada:
            total_clientes += 1
            cola.put(total_clientes)
            if tiempo_llegada == "a":
                llegada += valor_aleatorio(dist_llegada, min_lleg / 60, max_lleg / 60)
            else:
                llegada += const_lleg / 60

            if cliente_actual is None:
                if cola.qsize() > 0 and servidor_presente == 1:
                    cliente_actual = cola.get()
                    if tiempo_servicio == "a":
                        fin_servicio = tiempo + valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                    else:
                        fin_servicio = tiempo + const_serv / 60
            continue

        if tiempo == fin_servicio:
            atendidos += 1
            cliente_actual = None
            if cola.qsize() > 0 and servidor_presente == 1:
                cliente_actual = cola.get()
                if tiempo_servicio == "a":
                    fin_servicio = tiempo + valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                else:
                    fin_servicio = tiempo + const_serv / 60
            else:
                fin_servicio = float('inf')
            continue

        if tiempo == llegada_servidor:
            servidor_presente = 1
            llegada_servidor = float('inf')
            if tiempo_trabajo == "a":
                salida_servidor = tiempo + valor_aleatorio(dist_trabajo, min_trab / 60, max_trab / 60)
            else:
                salida_servidor = tiempo + const_trabajo / 60

            if cliente_actual is None:
                if cola.qsize() > 0:
                    cliente_actual = cola.get()
                    if tiempo_servicio == "a":
                        fin_servicio = tiempo + valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                    else:
                        fin_servicio = tiempo + const_serv / 60
            continue

        if tiempo == salida_servidor:
            servidor_presente = 0
            salida_servidor = float('inf')
            if tiempo_descanso == "a":
                llegada_servidor = tiempo + valor_aleatorio(dist_descanso, min_desc / 60, max_desc / 60)
            else:
                llegada_servidor = tiempo + const_descanso / 60
            fin_servicio = float('inf')
            continue

    print(tabulate(tabla, headers=columnas, tablefmt="fancy_grid", stralign="center"))

    num_iteracion = len(tabla)
    ultima_fila = tabla[-1]
    print(f"\nÚltima iteración (número de la iteración): {num_iteracion}")
    print(f"Hora Actual: {ultima_fila[0]}")
    print(f"H Próx.FS: {ultima_fila[2]}")
    print(f"Cola: {ultima_fila[5]}")
    print(f"PS: {ultima_fila[6]}")
    print(f"C_At: {ultima_fila[8]}")

simular()
