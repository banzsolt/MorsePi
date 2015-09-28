import RPi.GPIO as GPIO
import time

the_pin = 7
speed = 0.1

morse = {'a': '.-',
         'b': '-...',
         'c': '-.-.',
         'd': '-..',
         'e': '.',
         'f': '..-.',
         'g': '--.',
         'h': '....',
         'i': '..',
         'j': '.---',
         'k': '-.-',
         'l': '.-..',
         'm': '--',
         'n': '-.',
         'o': '---',
         'p': '.--.',
         'q': '--.-',
         'r': '.-.',
         's': '...',
         't': '-',
         'u': '..-',
         'v': '...-',
         'w': '.--',
         'x': '-..-',
         'y': '-.--',
         'z': '--..',
         '1': '.----',
         '2': '..---',
         '3': '...--',
         '4': '....-',
         '5': '.....',
         '6': '-....',
         '7': '--...',
         '8': '---..',
         '9': '----.',
         '0': '-----'}


def process(text):
    global speed
    for character in text:
        if character == ' ':
            time.sleep(7 * speed)
        else:
            for signal in morse[character.lower()]:
                if signal == '.':
                    short()
                else:
                    long()
                time.sleep(speed)


def setup():
    global the_pin
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(the_pin, GPIO.OUT)


def long():
    global the_pin, speed
    GPIO.output(the_pin, GPIO.HIGH)
    time.sleep(3 * speed)
    GPIO.output(the_pin, GPIO.LOW)


def short():
    global the_pin, speed
    GPIO.output(the_pin, GPIO.HIGH)
    time.sleep(speed)
    GPIO.output(the_pin, GPIO.LOW)

if __name__ == '__main__':
    setup()
    while 1:
        process('SOS')
        time.sleep(5)
    GPIO.cleanup()
