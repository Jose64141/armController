from arm import *
from os import system, name
clear = 'cls' if name == 'nt' else 'clear'



def start():
    ip = '192.168.1.194'
    arm = Arm(ip)
    system(clear)
    input('Bienvenido. Por favor aléjese del robot. \n Si está listo, presione Enter para conectarse al robot.')

    arm.initialize()

    while True:

        break