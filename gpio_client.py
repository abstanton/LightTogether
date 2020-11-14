# import RPi.GPIO as GPIO
import socket
import sys
import RPi.GPIO as gpio
import components

gpio.setmode(gpio.BOARD)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
button = components.Button(10)

server_address = ('localhost', 10000)
sock.connect(server_address)

while(True):
    try:
        pressed = button.getNext()
        data = 1 if pressed else 0
        message = [data]
        print("state: " + str(data))
        sock.sendall(bytes(message))
    except:
        print("failed")
