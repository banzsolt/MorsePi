import RPi.GPIO as GPIO
import time
import multiprocessing

out_pins = [7, 11, 13, 15, 16, 18, 22, 29]
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


def process(text, to_pin):
    global speed
    for character in text:
        if character == ' ':
            time.sleep(7 * speed)
        else:
            for signal in morse[character.lower()]:
                if signal == '.':
                    short(to_pin)
                else:
                    long(to_pin)
                time.sleep(speed)


def setup():
    global out_pins
    GPIO.setmode(GPIO.BOARD)
    for pin in out_pins:
        GPIO.setup(pin, GPIO.OUT)


def long(to_pin):
    global speed
    GPIO.output(to_pin, GPIO.HIGH)
    time.sleep(3 * speed)
    GPIO.output(to_pin, GPIO.LOW)


def short(to_pin):
    global speed
    GPIO.output(to_pin, GPIO.HIGH)
    time.sleep(speed)
    GPIO.output(to_pin, GPIO.LOW)

if __name__ == '__main__':
    global out_pins
    setup()
    output = multiprocessing.Queue()
    
    while 1:
        processes = []
        for pin in out_pins:
            processes.append(multiprocessing.Process(target=process, args=('Zsolti', pin,)))
        
        i = 0
        while (i < len(processes)):
            processes[i].start()
            i += 1
        i = 0
        while (i < len(processes)):
            processes[i].join()
            i += 1
            
        time.sleep(1.5)
        
    GPIO.cleanup()
