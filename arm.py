from enum import IntEnum
from xarm import *


class ErrorType(IntEnum):
    API = 0
    MACHINE = 1


class CommandException(Exception):
    def __init__(self, code, message='The robot thrown an error.', type=0):
        self.code = code
        self.message = message + f' Error code: {code}'
        self.type = type


# Components of the cartesian position vector
class Components(IntEnum):
    X = 0
    Y = 1
    Z = 2
    ROLL = 3
    PITCH = 4
    YAW = 5


class Modes(IntEnum):
    LINEAR = 0
    JOINT = 1
    TRAIN = 2


class Sensitivities(IntEnum):
    TEACH = 0
    COLLISION = 1


class Arm:
    # Constructor
    def __init__(self, ipAddress):
        self.ip = ipAddress
        self.servos = [0 for i in range(6)]
        self.position = [0 for i in range(7)]
        self.sensitivities = [1 for i in range(3)]
        self.mode = Modes.LINEAR
        self.wrapper = XArmAPI(ipAddress, do_not_open=True)

    def __sanity_check(self):
        if not self.wrapper.connected:
            raise RuntimeError('The arm is not connected!')
        if self.wrapper.has_error:
            error = self.wrapper.error_code
            raise CommandException(error, f'The controller reported an error! Please review and clean. \n')

    # Enter linear movement mode
    ## Note: In the xArm 5, cartesian movement limits the roll and pitch to +-180° and 0° respectively, so it will reset to that orientation.
    def __switch_to_linear(self):
        status_code = self.wrapper.set_mode(Modes.LINEAR)
        self.mode = Modes.LINEAR

    # Enter joint training mode (LEARN HOW TO TRAIN/RECORD)
    def __switch_to_training(self):
        status_code = self.wrapper.set_mode(Modes.TRAIN)
        self.mode = Modes.TRAIN

    # Establish xArm connection, enter joint training mode for testing
    def initialize(self):
        self.wrapper.connect()
        self.wrapper.motion_enable(enable=True)
        self.__switch_to_training()
        self.wrapper.set_state(state=0)

    # Disconnect arm
    def disconnect(self):
        self.wrapper.disconnect()

    # Sends a (soft) emergency stop signal to the arm ()
    def emergency_stop(self):
        self.wrapper.emergency_stop()

    # Given a movement vector, set the new position of the arm
    def move_arm(self, delta):
        new_position = [self.position[i] + delta[i] for i in range(len(self.position))]
        # Using relative movement (?
        status_code = self.wrapper.set_position(x=new_position[Components.X],
                                                y=new_position[Components.Y],
                                                z=new_position[Components.Z],
                                                roll=new_position[Components.ROLL],
                                                yaw=new_position[Components.YAW],
                                                pitch=new_position[Components.PITCH],
                                                wait=False)
        if status_code < 0:
            raise CommandException(status_code)

        status_code, resulting_position = self.wrapper.get_position()
        if status_code != 0:
            raise CommandException(status_code)
        self.position = resulting_position

    # Move all servos by a certain degree each
    def move_servos(self, delta, servo_id=None):
        new_servos = [self.servos[i] + delta[i] for i in range(len(self.servos))] if servo_id is None else delta
        status_code = self.wrapper.set_servo_angle(angle=new_servos, servo_id=servo_id, wait=False)
        if status_code < 0:
            raise CommandException(status_code)

        status_code, resulting_servos = self.wrapper.get_servo_angle()
        if status_code != 0:
            raise CommandException(status_code)
        self.servos = resulting_servos

    # Switch arm operation mode
    def switch_mode(self, mode):
        self.wrapper.set_state(4)
        if mode == Modes.LINEAR:
            self.__switch_to_linear()
        elif mode == Modes.TRAIN:
            self.__switch_to_training()
        else:
            pass
        self.wrapper.set_state(0)

    # Clean the robot errors and re-enable movement
    def clean_errors(self):
        self.wrapper.clean_error()
        self.wrapper.clean_gripper_error()
        # Re-enabling robot movement (as per User Manual)
        self.wrapper.motion_enabled(True)
        self.wrapper.set_state(0)
# Singularity should be addressed3
