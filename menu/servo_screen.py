from arm import *
from os import system, name

clear = 'cls' if name == 'nt' else 'clear'
step = 1  # Servo rotation degree step

class ServoScreen:
    def __init__(self, arm, parent):
        self.arm = arm
        self.parent = parent
        self.servos = []
        self.current_servo = 0
        self.showing = False

    def __handle_move(self, decrease):
        delta = -step if decrease else step
        delta += self.servos[self.current_servo]
        self.arm.move_servos(delta, self.current_servo)
        self.servos = self.arm.servos

    # Print screen
    def print_screen(self):
        system(clear)
        print('Servos: [ ', end='')
        for i in range(len(self.servos)):
            character = '█ ' if self.current_servo == i else '░ '
            print(character, end='')
        print(f' ] | Servo actual: {self.current_servo} | Incremento actual: {self.step}°')

        print(f'Posición de servo actual: {self.servos[self.current_servo]}')


    # Switch to this screen
    def show_screen(self):
        self.servos = self.arm.servos
        self.showing = True
        self.arm.switch_mode(Modes.LINEAR)
