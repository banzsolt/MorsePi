import RPi.GPIO as GPIO
import time
import multiprocessing

speed = 0.1
data = {'3': 'e  e    e  e              t t',
        '5': '                      e',
        '7': ' e  e    e  e           e',
        '8': '                  e  e',
        '10': '    t t     t t    e  e',
        '11': '                e   e',
        '12': '               e',
        '13': '              e',
        '15': '',
        '16': '',
        '18': '',
        '19': '',
        '21': '',
        '22': '',
        '23': '',
        '24': '',
        '26': '',
        '29': '',
        '31': '',
        '32': '',
        '33': '',
        '35': '',
        '36': '',
        '37': '',
        '38': '',
        '40': ''}
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


def process(the_text, to_pin):
    global speed
    for character in the_text:
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
    global data
    GPIO.setmode(GPIO.BOARD)
    for pin, value in data.iteritems():
        GPIO.setup(int(pin), GPIO.OUT)


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
    global data
    setup()
    output = multiprocessing.Queue()
    
    while 1:
        processes = []
        for pin_no, text in data.iteritems():
            processes.append(multiprocessing.Process(target=process, args=(text, int(pin_no),)))
        
        i = 0
        while i < len(processes):
            processes[i].start()
            i += 1
        i = 0
        while i < len(processes):
            processes[i].join()
            i += 1
            
        time.sleep(1.5)
        
    GPIO.cleanup()
