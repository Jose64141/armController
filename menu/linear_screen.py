from arm import *
from os import system, name

CLEAR = 'cls' if name == 'nt' else 'clear'
step = 5  # Linear movement mm step

class LinearScreen:
    def __init__(self, arm, parent):
        self.arm = arm
        self.parent = parent
        self.position = []
        self.current_mode = Modes.LINEAR
        self.showing = False

    def __handle_move(self, movement):
        delta = [movement[i]*step for i in range(len(self.position))]
        self.arm.move_linear(delta)
        self.position = self.arm.position

    # Print screen
    def print_screen(self):
        system(CLEAR)
        print('Posición: [ ', end='')
        for i in range(len(self.position)):
            character = '█ ' if self.current_servo == i else '░ '
            print(character, end='')
        print(f' ] | Servo actual: {self.current_servo} | Incremento actual: {self.step}°')

        print(f'Posición de servo actual: {self.servos[self.current_servo]}')


    # Switch to this screen
    def show_screen(self):
        self.servos = self.arm.servos
        self.showing = True
        self.arm.switch_mode(Modes.LINEAR)
