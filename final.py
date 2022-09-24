import threading 
import time

sillas = threading.Semaphore(4)

barberoListo = threading.Semaphore(1)

clienteListo = threading.Semaphore(1)
corteTerminado = threading.Semaphore(1)


sillasDisponibles = 4

TotalClientes = 0

def corteFinalizado():
    print('\nCorte finalizado\n')
    corteTerminado.release()


def cortarCabello():
    print('Se realiza la tarea')
    time.sleep(3)
    corteFinalizado()


def funcionBarbero():


    global TotalClientes

    while TotalClientes == 0:
        print('No hay clientes. el barbero espera')
    while TotalClientes > 0:
        clienteListo.acquire()
        global sillasDisponibles 
        print('\nEl barbero atiende al cliente')
        sillasDisponibles += 1
        sillas.release()
        print('Sillas disponibles: ', sillasDisponibles)
        print('nuemero de clientes (sumando al que está siendo atendido): ', TotalClientes)
        cortarCabello()
        barberoListo.release()
        TotalClientes -= 1
    

def funcionCliente(index):
    print('\nLlega cliente: ', index)
    global sillasDisponibles
    if(sillasDisponibles>0):
        sillas.acquire()
        sillasDisponibles -= 1
        global TotalClientes
        TotalClientes += 1
        print('El cliente se sienta en una silla')
        print('El está listo para recibir el corte')
        print('Sillas disponibles: ', sillasDisponibles)
        print('Total de clientes (sumando al que está siendo atendido): ', TotalClientes)
        clienteListo.release()
        corteTerminado.acquire()
        barberoListo.acquire()
    
    else:
        print('\nEl cliente se retira del lugar por que ya no hay espacio Disponible')

def main():
    while True:
        print(" por favor indica si quieres repetir el procedimiento(s/n)")
        barbero = threading.Thread(target=funcionBarbero)
        num = int(input("numero de clientes para ser antendidos: "))
        
        barbero.start()
        listaClientes = list()
        for index in range(num):
            c = threading.Thread(target=funcionCliente, args=(index+1,))
            listaClientes.append(c)
            time.sleep(1)
            c.start()
        time.sleep(3*num)
        value = input('¿Deseas repetir el prtocedimiento? s/n.\n')
        if(value == "S" or value == "N"):
            break

if __name__ == '__main__':
   main()
