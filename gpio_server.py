import RPi.GPIO as gpio
import socket
import sys

def setup(pin):
    gpio.setmode(gpio.BOARD)
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, False)

setup(36)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
sock.bind(server_address)

sock.listen(1)
connection, client_address = sock.accept()

while True:
    try:
        print('connection from ' + str(client_address))
        #Receive the data in small chunks and retransmit it
        
        data = connection.recv(16)
        state = int.from_bytes(data, "big")
        print('received "%d"' % int.from_bytes(data, "big"))
        if state == 1:
            gpio.output(36, True)
        elif state == 0:
            gpio.output(36, False)
    except:
        print("error")
            
    # finally:
    #     # Clean up the connection
    #     connection.close()