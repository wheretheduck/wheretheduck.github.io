import time
import RPi.GPIO as GPIO
from clocko import*
GPIO.setmode(GPIO.BCM)

_forward = 5
_backward = 6
_right = 13
_left = 19
_stop = 26

_last_stop = 0

_all_pins = [_forward, _backward, _right, _left, _stop]

_current_pin = None

TIME_DELAY = 500

for pin in _all_pins:
    print(pin)
    GPIO.setup(pin, GPIO.OUT)

def _sleep():
    time.sleep(1)

def _turnPinOn(pin_num):
    GPIO.output(pin_num, GPIO.HIGH)
def _turnPinOff(pin_num):
    global _current_pin
    GPIO.output(pin_num, GPIO.LOW)
    if pin_num == _current_pin:
        _current_pin = None
def _turnAllPinsOff():
    for pin in _all_pins:
        _turnPinOff(pin)


def _dothedo(pin):
    global _current_pin
    global _last_stop
    if pin != _stop:
        if not hasStopped():
            stop()
        while getTime() - _last_stop < TIME_DELAY:
            pass
    _turnAllPinsOff()
    _turnPinOn(pin)
    _current_pin = pin

def stop():
    global _last_stop
    print(":stop")
    _last_stop = getTime()
    if not hasStopped():
        _dothedo(_stop)

def moveForward():
    print(":movf")
    if not movingForward():
        _dothedo(_forward)

def moveBackward():
    if not movingBackward():
        _dothedo(_backward)

def rotateLeft():
    print(":rotl")
    if not rotatingLeft():
        _dothedo(_left)

def rotateRight():
    print(":rotr")
    if not rotatingRight():
        _dothedo(_right)

def hasStopped():
    return _current_pin == _stop

def movingForward():
    return _current_pin == _forward

def movingBackward():
    return _current_pin == _backward

def rotatingLeft():
    return _current_pin == _left

def rotatingRight():
    return _current_pin == _right

stop()
if __name__ == "__main__":
    moveForward()
    rotateRight()
    moveForward()
    rotateRight()
    stop()

