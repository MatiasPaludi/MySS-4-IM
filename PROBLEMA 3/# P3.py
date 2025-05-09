import queue
import random
from tabulate import tabulate

def strftime_a_min(hora):
    h, m, s = map(int, hora.split(":"))
    return h * 60 + m + s / 60

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

    tiempo_max_espera = int(input("Tiempo máximo de espera en cola (segundos): ")) / 60

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
    tiempos_entrada_cola = {}
    abandonos = 0
    registro_abandonos = []

    for i in range(en_cola):
        cliente_id = i + 1
        cola.put(cliente_id)
        tiempos_entrada_cola[cliente_id] = hora_ini

    if ps_ocupado == 1:
        cliente_actual = en_cola + 1
    else:
        cliente_actual = -1  # -1 indica que no hay cliente atendiendo

    atendidos = 0
    total_clientes = en_cola
    if ps_ocupado == 1:
        total_clientes += 1

    tabla = []
    columnas = ["Hora Actual", "H Próx.LLC", "H Próx.FS", "Cola", "PS", "C_At", "N° abandono","c_abandono"]

    tabla.append([
        min_a_strftime(tiempo),
        min_a_strftime(llegada),
        min_a_strftime(fin_servicio),
        cola.qsize(),
        1 if cliente_actual > 0 else 0,
        atendidos,
        abandonos
    ])

    while tiempo <= hora_fin:
        # Verificar abandonos
        cola_tmp = queue.Queue()
        c_abandono = ""  # Variable para registrar el cliente que abandonó
        while cola.qsize() > 0:
            cliente = cola.get()
            tiempo_espera = tiempo - tiempos_entrada_cola[cliente]
            if tiempo_espera >= tiempo_max_espera:
                abandonos += 1
                registro_abandonos.append((cliente, tiempos_entrada_cola[cliente], tiempo))
                tiempos_entrada_cola.pop(cliente)
                c_abandono = f"Cliente {cliente}"  # Registra el cliente que abandonó
            else:
                cola_tmp.put(cliente)
        cola = cola_tmp

        if llegada <= fin_servicio:
            tiempo = llegada
            if tiempo > hora_fin:
                break
            total_clientes += 1
            cola.put(total_clientes)
            tiempos_entrada_cola[total_clientes] = tiempo

            if tiempo_llegada == "a":
                llegada += valor_aleatorio(dist_llegada, min_lleg / 60, max_lleg / 60)
            else:
                llegada += const_lleg / 60

            if cliente_actual <= 0:
                if cola.qsize() > 0:
                    nuevo = cola.get()
                    cliente_actual = nuevo
                    tiempos_entrada_cola.pop(nuevo)
                    if tiempo_servicio == "a":
                        fin_servicio = tiempo + valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                    else:
                        fin_servicio = tiempo + const_serv / 60
        else:
            tiempo = fin_servicio
            if tiempo > hora_fin:
                break
            atendidos += 1
            cliente_actual = -1

            if cola.qsize() > 0:
                nuevo = cola.get()
                cliente_actual = nuevo
                tiempos_entrada_cola.pop(nuevo)
                if tiempo_servicio == "a":
                    fin_servicio = tiempo + valor_aleatorio(dist_serv, min_serv / 60, max_serv / 60)
                else:
                    fin_servicio = tiempo + const_serv / 60
            else:
                fin_servicio = float('inf')

        tabla.append([
            min_a_strftime(tiempo),
            min_a_strftime(llegada),
            min_a_strftime(fin_servicio),
            cola.qsize(),
            1 if cliente_actual > 0 else 0,
            atendidos,
            abandonos,
            c_abandono
        ])

    print(tabulate(tabla, headers=columnas, tablefmt="fancy_grid", stralign="center"))
    print(f"\nTotal de abandonos: {abandonos}")

    if abandonos > 0:
        print("\nDetalle de abandonos (Cliente, Hora entrada cola, Hora abandono):")
        for cli, h_ent, h_sal in registro_abandonos:
            print(f"Cliente {cli}: {min_a_strftime(h_ent)} -> {min_a_strftime(h_sal)}")

    input("\nPresione Enter para salir...")

simular()
