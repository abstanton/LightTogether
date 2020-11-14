import RPi.GPIO as gpio
import socket
import sys
import time
import keyboard
import threading
import os

ip_address = str(sys.argv[1])
light_pin = int(sys.argv[2])

play = True

def setup(pin):
    gpio.setmode(gpio.BOARD)

setup(light_pin)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip_address, 10000)
sock.bind(server_address)

sock.listen(1)

connections = []
threads = []

pins = [32, 36]

def process_connection(connection, pin):
    global play
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, False)
    while play:
        try:
            #Receive the data in small chunks and retransmit it
            data = connection.recv(16)
            state = int.from_bytes(data, "big")
            print('received "%d"' % int.from_bytes(data, "big"))
            if state == 1:
                gpio.output(pin, True)
            elif state == 0:
                gpio.output(pin, False)
        except:
            connection.close()
            exit()
    connection.close()
    exit()
          
def get_connections():
    global connections
    global pins
    global threads
    curr_pin = 0
    global sock
    while True:
        try:
            print("waiting...")
            connection, address = sock.accept()
            connections.append(connection)
            thread = threading.Thread(target=process_connection, args=[connection, pins[curr_pin]])
            threads.append(thread)
            curr_pin += 1
            thread.start()
        except:
            print("error accepting client")

connection_thread = threading.Thread(target=get_connections)
connection_thread.start()

while True:
    if keyboard.is_pressed('q'):
        sock.close()
        for c in connections:
            c.close()
        for t in threads:
            t.join()
        play = False
        time.sleep(2)
        #quit()    
        os._exit(1)