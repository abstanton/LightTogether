# import RPi.GPIO as GPIO
import socket
import sys
import RPi.GPIO as gpio
import components


ip_address = str(sys.argv[1])
button_pin = int(sys.argv[2])


gpio.setmode(gpio.BOARD)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
button = components.Button(button_pin)

server_address = (ip_address, 10000)
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
