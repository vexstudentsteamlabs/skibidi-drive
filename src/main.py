
# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Areng                                                        #
# 	Created:      6/1/2024, 2:55:59 PM                                         #
# 	Description:  skibididrivetraindopdopyesyes                                #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

#define motor ports
drive_ports = (Ports.PORT17,
               Ports.PORT19,
               Ports.PORT18,
               Ports.PORT20)

#Inititlize everything

#Define motor groups
d_lfor = Motor(drive_ports[0]) #left forwards
d_rfor = Motor(drive_ports[1]) #right forwards
d_lbac = Motor(drive_ports[2]) #left backwards
d_rbac = Motor(drive_ports[3]) #right backwards

#group em motors
leftm = MotorGroup(d_lfor,d_lbac)
rightm = MotorGroup(d_rfor,d_rbac)

#define controller
control = Controller()

multi = 20 #Sensitive amount. The more the more sensitive

#get gps
gps = Gps(Ports.PORT15)


#TODO: implement auton

# Helper function to move robot forward/backward or turn.
def move(left_speed: int, right_speed: int, duration: int):
    leftm.set_velocity(left_speed, PERCENT)
    rightm.set_velocity(right_speed, PERCENT)
    leftm.spin(FORWARD)
    rightm.spin(FORWARD)
    wait(duration, MSEC)
    leftm.stop()
    rightm.stop()

def turn(degrees: float, speed: int = 50):
    """
    Function to turn robot by a specific number of degrees.
    Positive for clockwise, negative for counterclockwise.
    """
    if degrees > 0:
        leftm.set_velocity(speed, PERCENT)
        rightm.set_velocity(-speed, PERCENT)
    else:
        leftm.set_velocity(-speed, PERCENT)
        rightm.set_velocity(speed, PERCENT)
        
    leftm.spin(FORWARD)
    rightm.spin(FORWARD)
    wait(abs(degrees) * 10, MSEC)  # Estimate time for turn based on degrees
    leftm.stop()
    rightm.stop()

def realign():
    turnvelo = 50
    while abs(gps.rotation()) > 2:  # Tolerance of 2 degrees
        if gps.rotation() > 0:
            leftm.set_velocity(turnvelo, PERCENT)
            rightm.set_velocity(-turnvelo, PERCENT)
        else:
            leftm.set_velocity(-turnvelo, PERCENT)
            rightm.set_velocity(turnvelo, PERCENT)
        leftm.spin(FORWARD)
        rightm.spin(FORWARD)
        wait(50, MSEC)
        leftm.stop()
        rightm.stop()
        turnvelo -= 5
    leftm.stop()
    rightm.stop()

# Autonomous routine
def autoton() -> None:
    gps.reset_rotation()
    
    # List of steps for autonomous
    steps = [
        {"move": (100, 50), "duration": 1000, "realign_after": True},
        {"move": (80, 80), "duration": 2000, "realign_after": False},
        {"turn": 90, "realign_after": False},
        {"intake": True, "duration": 2000},
        {"move": (100, 100), "duration": 1500, "realign_after": True}
    ]

    for step in steps:
        if "move" in step:
            move(step["move"][0], step["move"][1], step["duration"])
        
        if "turn" in step:
            turn(step["turn"])
        
        if "intake" in step:
            wheeldown()
            intake()
            wait(step["duration"])
            wheeldown()
            intake()

        if step.get("realign_after", False):
            realign()
        
        wait(100, MSEC)  # Optional wait between steps



def driver():
    global multi
    #Continuely listen to controller
    while True:
        axises = [
            round(control.axis2.position() / 10) * -1,
            round(control.axis3.position() / 10) * -1,
        ] #Store the axis into a list
        """
        Divide by 10 for chunking and multiply by -1 to reverse

        """


        """
        Spin the motors. just randomize reverse forward until they seem to be
        driving correctly. if it works, dont change it
        """
        leftm.spin(REVERSE,axises[0] * multi)
        rightm.spin(FORWARD,axises[1] * multi)
    
Thread(driver)

#Basic drivetrain complete
#do more stuff

def shakeit():
    leftm.spin(REVERSE,-100)
    rightm.spin(FORWARD,-100)
    wait(50)
    leftm.spin(REVERSE,100)
    rightm.spin(FORWARD,100)
    wait(50)
    #await testing.

control.buttonA.pressed(shakeit)  

pist1 = DigitalOut(brain.three_wire_port.h)
pist2 = DigitalOut(brain.three_wire_port.g)

isgripping = False
def grip():
    #toggle
    global isgripping,pist1,pist2
    if not isgripping:
        pist1.set(True)                                          
        isgripping = True
    else:
        pist1.set(False)
        isgripping = False

isgripping2 = False
def grip2():
    #toggle
    global isgripping2,pist1,pist2
    if not isgripping2:
        pist2.set(True)                                          
        isgripping2 = True
    else:
        pist2.set(False)
        isgripping2 = False

control.buttonL1.pressed(grip)  

control.buttonL2.pressed(grip2)  
pist3 = DigitalOut(brain.three_wire_port.f)
isintakeready = False
motorintakem = Motor(Ports.PORT4)
motorintake2 = Motor(Ports.PORT5)

toggle124 = False
def wheeldown():
    #toggle
    global toggle124
    if not toggle124:
        pist3.set(True)                                          
        toggle124 = True
    else:
        pist3.set(False)
        toggle124 = False
 
def intake():
    #toggle
    global isintakeready
    if not isintakeready:
        motorintakem.spin(FORWARD,600)
        motorintake2.spin(REVERSE,600)
        isintakeready = True
    else:
        motorintakem.stop()
        motorintake2.stop()
        isintakeready = False

control.buttonR2.pressed(wheeldown)  
control.buttonR1.pressed(intake)  