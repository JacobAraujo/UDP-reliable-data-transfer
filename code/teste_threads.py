import threading
import time

# Variável flag para alternar entre as threads
executar_thread1 = True

# Semáforo binário para controlar o acesso à flag
semaphore = threading.Semaphore()

# Função para a primeira thread
def thread1():
    global executar_thread1
    while True:
        with semaphore:
            if executar_thread1:
                print("Executando Thread 1")
                time.sleep(2)
                executar_thread1 = False

# Função para a segunda thread
def thread2():
    global executar_thread1
    while True:
        with semaphore:
            if not executar_thread1:
                print('Executando Thread 2')
                time.sleep(2)
                executar_thread1 = True
            

# Iniciar as threads
t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)
t1.start()
t2.start()
