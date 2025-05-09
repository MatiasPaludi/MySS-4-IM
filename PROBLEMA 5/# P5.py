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
    elif distrib == "exponencial":
        return random.expovariate(1 / ((minimo + maximo) / 2))
    elif distrib == "normal":
        return random.gauss((minimo + maximo) / 2, (maximo - minimo) / 6)
    return (minimo + maximo) / 2

def simular():
    hora_ini = strftime_a_min(input("Hora de inicio (HH:MM:SS): "))
    hora_fin = strftime_a_min(input("Hora de fin (HH:MM:SS): "))

    tipo_llegada = input("¿Hora de llegada de cliente aleatoria o constante? (a/c): ").lower()
    if tipo_llegada == "a":
        dist_llegada = input("Distribución (uniforme, exponencial, normal): ").lower()
        min_lleg = int(input("Rango mínimo en segundos : "))
        max_lleg = int(input("Rango máximo en segundos : "))
    else:
        const_lleg = int(input("Hora de llegada de cliente constante en segundos: "))

    tipo_servicio = input("¿Tiempo de servicio aleatorio o constante? (a/c): ").lower()
    if tipo_servicio == "a":
        dist_serv = input("Distribución (uniforme, exponencial, normal): ").lower()
        min_serv = int(input("Rango mínimo en segundos : "))
        max_serv = int(input("Rango máximo en segundos : "))
    else:
        const_serv = int(input("Tiempo de servicio constante (segundos): "))

    tipo_espera_zn = input("¿Tiempo de espera en ZN aleatorio o constante? (a/c): ").lower()
    if tipo_espera_zn == "a":
        dist_zn = input("Distribución (uniforme, exponencial, normal): ").lower()
        min_zn = int(input("Rango mínimo de espera en ZN (segundos): "))
        max_zn = int(input("Rango máximo de espera en ZN (segundos): "))
    else:
        const_zn = int(input("Tiempo de espera constante en ZN (segundos): "))

    en_cola = int(input("Clientes inicialmente en cola: "))
    ps_ocupado = int(input("¿Puesto de servicio ocupado al inicio? (1=sí, 0=no): "))
    llegada_inicial = strftime_a_min(input("Hora inicial de próxima llegada (HH:MM:SS): "))
    fin_servicio_inicial = float('inf')
    if ps_ocupado == 1:
        fin_servicio_inicial = strftime_a_min(input("Hora inicial de próximo fin de servicio (HH:MM:SS): "))

    tiempo = hora_ini
    llegada = llegada_inicial
    fin_servicio = fin_servicio_inicial
    cola = queue.Queue()
    for i in range(en_cola):
        cola.put(i + 1)

    zona_seguridad = 0
    PS = 1 if ps_ocupado else 0
    fin_espera_zn = float('inf')
    cliente_actual = None
    cliente_en_zn = None
    total_clientes = en_cola
    atendidos = 0

    tabla = []
    columnas = [
        "Iteración", "Hora Actual", "H Próx.LLC", "H Próx.FS", "Cola",
        "ZN", "PS", "H Lleg. a ZN", "H Lleg. a PS", "C_At", "Espera ZN", "Cliente en PS"
    ]

    hora_llegada_zn = float('inf')
    hora_llegada_ps = float('inf')
    espera_zn_min = 0.0
    iteracion = 1

    tabla.append([
        iteracion,
        min_a_strftime(tiempo),
        min_a_strftime(llegada),
        min_a_strftime(fin_servicio),
        cola.qsize(),
        zona_seguridad,
        PS,
        min_a_strftime(hora_llegada_zn),
        min_a_strftime(hora_llegada_ps),
        atendidos,
        min_a_strftime(espera_zn_min),
        cliente_en_zn if cliente_en_zn is not None else "----"
    ])

    while tiempo <= hora_fin:
        iteracion += 1
        tiempo = min(llegada, fin_espera_zn, fin_servicio)

        if tiempo == llegada:
            total_clientes += 1
            if PS == 0 and zona_seguridad == 0 and cola.qsize() > 0:
                cliente_actual = cola.get()
                zona_seguridad = 1
                hora_llegada_zn = tiempo
                espera_zn_min = valor_aleatorio(dist_zn, min_zn / 60, max_zn / 60) if tipo_espera_zn == "a" else const_zn / 60
                fin_espera_zn = tiempo + espera_zn_min
                hora_llegada_ps = fin_espera_zn
                fin_servicio = float('inf')  # Se asignará cuando realmente entre al PS
            else:
                cola.put(total_clientes)
                hora_llegada_zn = float('inf')
                hora_llegada_ps = float('inf')
                espera_zn_min = 0.0

            llegada += valor_aleatorio(dist_llegada, min_lleg / 60, max_lleg / 60) if tipo_llegada == "a" else const_lleg / 60

        elif tiempo == fin_espera_zn:
            PS = 1
            zona_seguridad = 0
            cliente_en_zn = cliente_actual
            cliente_actual = None
            fin_espera_zn = float('inf')

            fin_servicio = tiempo + (valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                                     if tipo_servicio == "a" else const_serv / 60)

        elif tiempo == fin_servicio:
            PS = 0
            atendidos += 1
            cliente_en_zn = None
            hora_llegada_zn = float('inf')
            hora_llegada_ps = float('inf')
            espera_zn_min = 0.0

            if cola.qsize() > 0:
                cliente_actual = cola.get()
                zona_seguridad = 1
                hora_llegada_zn = tiempo
                espera_zn_min = valor_aleatorio(dist_zn, min_zn / 60, max_zn / 60) if tipo_espera_zn == "a" else const_zn / 60
                fin_espera_zn = tiempo + espera_zn_min
                hora_llegada_ps = fin_espera_zn
                fin_servicio = float('inf')

        tabla.append([
            iteracion,
            min_a_strftime(tiempo),
            min_a_strftime(llegada),
            min_a_strftime(fin_servicio),
            cola.qsize(),
            zona_seguridad,
            PS,
            min_a_strftime(hora_llegada_zn),
            min_a_strftime(hora_llegada_ps),
            atendidos,
            min_a_strftime(espera_zn_min),
            cliente_en_zn if cliente_en_zn is not None else "----"
        ])

    print(tabulate(tabla, headers=columnas, tablefmt="fancy_grid", stralign="center"))

    ultima_iteracion = len(tabla)
    ultima_fila = tabla[-1]
    print(f"\nÚltima iteración (número {ultima_iteracion}):")
    for nombre_col, valor in zip(columnas, ultima_fila):
        print(f"{nombre_col}: {valor}")

    for fila in reversed(tabla):
        hora_min = strftime_a_min(fila[1])  # Cambió el índice por columna "Hora Actual"
        if hora_min <= hora_fin:
            print(f"\nÚltima fila dentro del tiempo de simulación (≤ {min_a_strftime(hora_fin)}):")
            print(tabulate([fila], headers=columnas, tablefmt="fancy_grid", stralign="center"))
            break
simular()
input("\nPresione Enter para salir...")

