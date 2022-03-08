# HOJA DE TRABAJO 5
# ESTRUCTURAS DE DATOS 
# SIMULADOR DE PROGRAMAS EN EJECUCION EN UNA COMPUTADORA
# GRUPO 1. JUAN PABLO CORDON,  ROBERTO  RIOS, XIMENA LOARCA

import simpy
import random

env = simpy.Environment() #ambiente de simulación

CPU = simpy.Resource(env,capacity = 1) # cola de CPU
RAM = simpy.Container(env, init=100, capacity=100) #cola de RAM
I_O = simpy.Resource(env,capacity = 1) #cola de waiting para hacer operaciones de I/O

random.seed(10) # fijar el inicio de random

def programa(nombre, env, hora_llegada, RAM, CPU):
    global totalDia
    
    memoria = random.randint(1,10)
    instrucciones = random.randint(1,10)

    #cuando el proceso entra a la cola de NEW
    yield env.timeout(hora_llegada)
    

    print("%f %s NEW a las %f, ocupa %i de memoria y tiene %i instrucciones" % (env.now, nombre, hora_llegada, memoria, instrucciones))
    
    #cuando el proceso ya tiene espacio de memoria y entra a la cola de ready
    yield RAM.get(memoria)
    print("%f %s: READY ya caben sus %i de memoria" % (env.now, nombre, memoria))

    while instrucciones > 0:
        #esperar a que CPU pueda manejar el proceso
        with CPU.request() as running:
            yield running
            print("%f %s cpu disponible" %(env.now, nombre))
            #simulamos que tardamos 1 unidad de tiempo realizando 3 instrucciones
            instrucciones -= 3
            tiempoRun = 1
            yield env.timeout(tiempoRun)
            
        print ("%f %s: ejecutado instrucciones " % (env.now, nombre))

        if instrucciones > 0:
            caso = random.randint(1,2)
            if caso == 1:
                print ("%f %s: regresa a READY con %i pendientes" % (env.now, nombre, instrucciones))
            elif caso == 2:
                print ("%f %s: entra a WAITING para operaciones de I/O" % (env.now, nombre))
                with I_O.request() as waiting:
                    yield waiting
                    tiempoIO = 1
                    yield env.timeout(tiempoIO)
                print ("%f %s: regresa a READY con %i pendientes" % (env.now, nombre, instrucciones))
    
    
    print ('%f %s TERMINATED sale del CPU y libera %i de memoria' % (env.now, nombre, memoria))       
    RAM.put(memoria)

    tiempoTotal = env.now - hora_llegada
    print ('%s tarda %f' % (nombre, tiempoTotal))
    totalDia = totalDia + tiempoTotal

# ----------------------



totalDia = 0
num_programas = 25
for i in range(num_programas):
    tiempo_llegada = random.expovariate(1.0/10)
    print("programa %d llegara a las %f" %(i,tiempo_llegada))
    env.process(programa('programa %d'%i,env, tiempo_llegada, RAM, CPU))

env.run()  #correr la simulación hasta el tiempo = 50

print ("tiempo promedio por programa es: ", totalDia/num_programas)
