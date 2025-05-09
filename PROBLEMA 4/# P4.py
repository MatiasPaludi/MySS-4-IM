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
    return str(horas).zfill(2) + ":" + str(minutos).zfill(2) + ":" + str(segundos).zfill(2)

def valor_aleatorio(distrib, minimo, maximo):
    if distrib == "uniforme":
        return random.uniform(minimo, maximo)
    if distrib == "exponencial":
        return random.expovariate(1 / ((minimo + maximo) / 2))
    if distrib == "normal":
        return random.gauss((minimo + maximo) / 2, (maximo - minimo) / 6)
    return (minimo + maximo) / 2

def simular():
    hora_ini = strftime_a_min(input("Hora de inicio de simulación (HH:MM:SS): "))
    hora_fin = strftime_a_min(input("Hora de fin de simulación (HH:MM:SS): "))

    # Llega cliente A
    tipo_llegada_A = input("¿Tiempo entre llegadas de cliente A aleatorio o constante? (a/c): ").lower()
    dist_llegada_A = ""
    min_lleg_A = max_lleg_A = const_lleg_A = 0
    if tipo_llegada_A == "a":
        dist_llegada_A = input("Distribución llegadas A (uniforme, exponencial, normal): ").lower()
        min_lleg_A = int(input("Tiempo mínimo entre llegadas A (segundos): "))
        max_lleg_A = int(input("Tiempo máximo entre llegadas A (segundos): "))
    if tipo_llegada_A == "c":
        const_lleg_A = int(input("Intervalo constante de llegada A (segundos): "))

    # Llega cliente B
    tipo_llegada_B = input("¿Tiempo entre llegadas de cliente B aleatorio o constante? (a/c): ").lower()
    dist_llegada_B = ""
    min_lleg_B = max_lleg_B = const_lleg_B = 0
    if tipo_llegada_B == "a":
        dist_llegada_B = input("Distribución llegadas B (uniforme, exponencial, normal): ").lower()
        min_lleg_B = int(input("Tiempo mínimo entre llegadas B (segundos): "))
        max_lleg_B = int(input("Tiempo máximo entre llegadas B (segundos): "))
    if tipo_llegada_B == "c":
        const_lleg_B = int(input("Intervalo constante de llegada B (segundos): "))

    # Servicio de clientes
    tipo_servicio = input("¿Tiempo de servicio aleatorio o constante? (a/c): ").lower()
    dist_serv = ""
    min_serv = max_serv = const_serv = 0
    if tipo_servicio == "a":
        dist_serv = input("Distribución servicio (uniforme, exponencial, normal): ").lower()
        min_serv = int(input("Tiempo mínimo de servicio (segundos): "))
        max_serv = int(input("Tiempo máximo de servicio (segundos): "))
    if tipo_servicio == "c":
        const_serv = int(input("Tiempo constante de servicio (segundos): "))

    # Espera clientes A
    tipo_espera_A = input("¿Tiempo máximo de espera de cliente A aleatorio o constante? (a/c): ").lower()
    dist_esp_A = ""
    min_esp_A = max_esp_A = const_esp_A = 0
    if tipo_espera_A == "a":
        dist_esp_A = input("Distribución espera A (uniforme, exponencial, normal): ").lower()
        min_esp_A = int(input("Tiempo mínimo espera A (segundos): "))
        max_esp_A = int(input("Tiempo máximo espera A (segundos): "))
    if tipo_espera_A == "c":
        const_esp_A = int(input("Tiempo constante espera A (segundos): "))

    # Espera clientes B
    tipo_espera_B = input("¿Tiempo máximo de espera de cliente B aleatorio o constante? (a/c): ").lower()
    dist_esp_B = ""
    min_esp_B = max_esp_B = const_esp_B = 0
    if tipo_espera_B == "a":
        dist_esp_B = input("Distribución espera B (uniforme, exponencial, normal): ").lower()
        min_esp_B = int(input("Tiempo mínimo espera B (segundos): "))
        max_esp_B = int(input("Tiempo máximo espera B (segundos): "))
    if tipo_espera_B == "c":
        const_esp_B = int(input("Tiempo constante espera B (segundos): "))

    clientes_A_iniciales = int(input("Cantidad de clientes A inicialmente en cola: "))
    clientes_B_iniciales = int(input("Cantidad de clientes B inicialmente en cola: "))

    ps_ocupado = int(input("¿Puesto de servicio ocupado al inicio? (1=sí, 0=no): "))
    llegada_inicial = strftime_a_min(input("Hora inicial de próxima llegada (HH:MM:SS): "))
    fin_servicio_inicial = float('inf')
    if ps_ocupado == 1:
        fin_servicio_inicial = strftime_a_min(input("Hora inicial de próximo fin de servicio (HH:MM:SS): "))

    tiempo = hora_ini
    llegada_A = llegada_inicial
    llegada_B = llegada_inicial
    fin_servicio = fin_servicio_inicial
    cola_A = queue.Queue()
    cola_B = queue.Queue()
    tiempos_entrada_A = {}
    tiempos_entrada_B = {}
    abandonos_A = []
    abandonos_B = []
    atendidos_A = 0
    atendidos_B = 0
    atendidos_totales = 0 
    abandonos_totales_A = 0  
    abandonos_totales_B = 0  

    cliente_id = 0

    for i in range(clientes_A_iniciales):
        cliente_id += 1
        cola_A.put(cliente_id)
        tiempos_entrada_A[cliente_id] = hora_ini


    for j in range(clientes_B_iniciales):
        cliente_id += 1
        cola_B.put(cliente_id)
        tiempos_entrada_B[cliente_id] = hora_ini

    
    # inicio el cliente actual
    if ps_ocupado == 1:
    # Si el puesto ya estaba ocupado, el cliente en servicio
    # será el siguiente ID que vamos a generar
        cliente_actual = cliente_id + 1
    else:
    # Si no, no hay cliente en servicio
        cliente_actual = -1

    atendidos = 0
    total_clientes = cliente_id
    total_clientes_en_cola = cola_A.qsize() + cola_B.qsize()

    tabla = []
    columnas = ["H. Actual", "H. Próx. LLC_A", "H. Próx. LLC_B", "H. Próx. FS", "QA", "QB", "Qt", "PS", "At_A", "At_B", "At_tot", "Ab_A", "Ab_B", "Ab_tot"]

    while tiempo <= hora_fin:
        evento = min(llegada_A, llegada_B, fin_servicio)
        tiempo = evento

        tiempo_max_espera_A = valor_aleatorio(dist_esp_A, min_esp_A, max_esp_A)/60 if tipo_espera_A == "a" else const_esp_A/60
        tiempo_max_espera_B = valor_aleatorio(dist_esp_B, min_esp_B, max_esp_B)/60 if tipo_espera_B == "a" else const_esp_B/60

    #Abandonos de clientes A (revisión)
        clientes_A = list(cola_A.queue)
        cola_A = queue.Queue()
        for cli in clientes_A:
            espera = tiempo - tiempos_entrada_A[cli]
            if espera >= tiempo_max_espera_A:
                abandonos_A.append((cli, tiempos_entrada_A[cli], tiempo))
                tiempos_entrada_A.pop(cli)
                total_clientes_en_cola -= 1
                abandonos_totales_A += 1
            else:
                cola_A.put(cli)

    #Abandonos de clientes B(revisión)
        clientes_B = list(cola_B.queue)
        cola_B = queue.Queue()
        for cli in clientes_B:
            espera = tiempo - tiempos_entrada_B[cli]
            if espera >= tiempo_max_espera_B:
                abandonos_B.append((cli, tiempos_entrada_B[cli], tiempo))
                tiempos_entrada_B.pop(cli)
                total_clientes_en_cola -= 1
                abandonos_totales_B += 1
            else:
                cola_B.put(cli)
    

        if evento == llegada_A:
            total_clientes += 1
            cliente_id = total_clientes
            cola_A.put(cliente_id)
            tiempos_entrada_A[cliente_id] = tiempo
            tiempo_llegada = valor_aleatorio(dist_llegada_A, min_lleg_A / 60, max_lleg_A / 60) if tipo_llegada_A == "a" else const_lleg_A / 60
            llegada_A += tiempo_llegada
            total_clientes_en_cola += 1
            if cliente_actual == -1 and not cola_A.empty():  #Si el servidor está libre (es decir, cliente_actual == -1) y si la cola A no está vacía , entonces el cliente que está en la cola A será atendido de inmediato
                cliente_actual = cola_A.get()
                tiempos_entrada_A.pop(cliente_actual)
                total_clientes_en_cola -= 1 # se atiende C_A de inmediato
                duracion_servicio = valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60) if tipo_servicio == "a" else const_serv / 60
                fin_servicio = tiempo + duracion_servicio
                atendidos_A += 1

        if evento == llegada_B:
            total_clientes += 1
            cliente_id = total_clientes
            cola_B.put(cliente_id)
            tiempos_entrada_B[cliente_id] = tiempo
            tiempo_llegada = valor_aleatorio(dist_llegada_B, min_lleg_B / 60, max_lleg_B / 60) if tipo_llegada_B == "a" else const_lleg_B / 60
            llegada_B += tiempo_llegada
            total_clientes_en_cola += 1
            # condicion para que solo C_B se atienda ni hay cliente A en cola y PS==0. cola_A.empty -> Qa ==0 
            if cliente_actual == -1 and cola_A.empty() and not cola_B.empty():
                cliente_actual = cola_B.get()
                tiempos_entrada_B.pop(cliente_actual)  # elimino el tiempo de entrada del cliente actual, porque fue atendido o salio de la cola
                total_clientes_en_cola -= 1
                duracion_servicio = valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60) if tipo_servicio == "a" else const_serv / 60
                fin_servicio = tiempo + duracion_servicio
                atendidos_B += 1

        if evento == fin_servicio:
            atendidos += 1
            cliente_actual = -1
            if cola_A.qsize() > 0:
                cliente_actual = cola_A.get()
                tiempos_entrada_A.pop(cliente_actual)
                duracion_servicio = valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60) if tipo_servicio == "a" else const_serv / 60
                fin_servicio = tiempo + duracion_servicio
                atendidos_A += 1
            else:
                if cola_B.qsize() > 0:
                    cliente_actual = cola_B.get()
                    tiempos_entrada_B.pop(cliente_actual)
                    duracion_servicio = valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60) if tipo_servicio == "a" else const_serv / 60
                    fin_servicio = tiempo + duracion_servicio
                    atendidos_B += 1
                else:
                    fin_servicio = float('inf')
        # calculo PS
        if cliente_actual != -1:
            puesto_ocupado = 1
        else:
            puesto_ocupado = 0
        
  

        tabla.append([ 
            min_a_strftime(tiempo),            #H. Actual
            min_a_strftime(llegada_A),         #H. prox. LLC_A
            min_a_strftime(llegada_B),         #H. prox. LLC_B
            min_a_strftime(fin_servicio),      #H. prox. FS
            cola_A.qsize(),                    #Clientes A en cola
            cola_B.qsize(),                    #Clientes B en cola
            cola_A.qsize() + cola_B.qsize(),   # Qt
            puesto_ocupado,                    #Estado de PS
            atendidos_A,                       #Clientes Atendidos A
            atendidos_B,                       #Clientes Atendidos B
            atendidos_A + atendidos_B,         # atendidos total 
            len(abandonos_A),                  #Cantidad de Abandonos en clientes A
            len(abandonos_B),                  #Cantidad de Abondonos en clientes B
            len(abandonos_A) + len(abandonos_B) # abandonos total
        ])

    print(tabulate(tabla, headers=columnas, tablefmt="fancy_grid", stralign="center"))

# imprimir la fila anterior o igual a la hora de fin de simulacion. (ultima fila valida dentro de la simulación)
  
    ultima_valida = None
    for fila in reversed(tabla):
        hora_fila = strftime_a_min(fila[0])
        if hora_fila <= hora_fin:
            ultima_valida = fila
            break

    if ultima_valida:
        print("\nÚltima iteración de la tabla (dentro del rango de simulación):")
        print(tabulate([ultima_valida], headers=columnas, tablefmt="fancy_grid", stralign="center"))

    if abandonos_A:
        tabla_ab_A = []
        for cli_id, h_llegada, h_abandono in abandonos_A:
            tabla_ab_A.append([f"cliente A {cli_id}", min_a_strftime(h_llegada), min_a_strftime(h_abandono)])
        print("\nAbandonos de clientes A:")
        print(tabulate(tabla_ab_A, headers=["N° cliente", "H. LLC", "H. Ab"], tablefmt="fancy_grid"))

    if abandonos_B:
        tabla_ab_B = []
        for cli_id, h_llegada, h_abandono in abandonos_B:
            tabla_ab_B.append([f"Cliente B {cli_id}", min_a_strftime(h_llegada), min_a_strftime(h_abandono)])
        print("\nAbandonos de Clientes B:")
        print(tabulate(tabla_ab_B, headers=["ID", "Hora Llegada", "Hora Abandono"], tablefmt="fancy_grid"))

    input("\nPresione Enter para salir...")

simular()
