import RPi.GPIO as GPIO
import time
import multiprocessing

speed = 0.1
data = {'3': 'Zsolti',
        '5': 'this is process which is longer',
        '7': 'Zsolti',
        '8': 'Zsolti',
        '10': 'Zsolti',
        '11': 'Zsolti',
        '12': 'Zsolti',
        '13': 'Zsolti',
        '15': 'Zsolti',
        '16': 'Zsolti',
        '18': 'Zsolti',
        '19': 'Zsolti',
        '21': 'Zsolti',
        '22': 'Zsolti',
        '23': 'Zsolti',
        '24': 'Zsolti',
        '26': 'Zsolti',
        '29': 'Zsolti',
        '31': 'Zsolti',
        '32': 'Zsolti',
        '33': 'Zsolti',
        '35': 'Zsolti',
        '36': 'Zsolti',
        '37': 'Zsolti',
        '38': 'Zsolti',
        '40': 'Zsolti'}
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
