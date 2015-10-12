import RPi.GPIO as GPIO
import time
import multiprocessing
import sys

args = sys.argv
parallel = False
same_output = True
speed = 0.025
data = {'3': 'SOS',
        '5': '',
        '7': '',
        '8': '',
        '10': '',
        '11': '',
        '12': '',
        '13': '',
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

def process_arguments():
    global args
    if len(args) == 0:
        return
    print(args)
    information = None
    last_option = None
    for argument in args:
        if '-' in argument:
            information[string(argument)] = None
            last_option = string(argument)
        if last_option is not None:
            information[last_option] = argument
    return  information

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


def on(to_pin):
    global speed
    GPIO.output(to_pin, GPIO.HIGH)
    time.sleep(speed)


def off(to_pin):
    global speed
    GPIO.output(to_pin, GPIO.LOW)
    time.sleep(speed)
    
    
if __name__ == '__main__':
    global data, parallel, same_output, args
    setup()
    test = process_arguments()
    print(test)

    while 1:
        processes = []
        helper = {'1': 7,
                  '2': 10,
                  '3': 11,
                  '4': 12,
                  '5': 13}
        # 1,2,3,4,5,5,4,3,2,1 - run till the end and back
        sequence = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
        
        for repeat in range (0, 3):
            for pin in sequence:
                processes.append(multiprocessing.Process(target=process, args=('e', helper[str(pin)],)))    
        
        # nice snaky flash
        for repeat in range (0,3):
            i = 1
            while i <= 5:
                processes.append(multiprocessing.Process(target=on, args=(helper[str(i)],)))
                i = i+1
                
            i = 1
            while i <= 5:
                processes.append(multiprocessing.Process(target=off, args=(helper[str(i)],)))
                i = i+1
                
        # nice snaky flash backwards
        for repeat in range (0,3):
            i = 5
            while i > 0:
                processes.append(multiprocessing.Process(target=on, args=(helper[str(i)],)))
                i = i-1
                
            i = 5
            while i > 0:
                processes.append(multiprocessing.Process(target=off, args=(helper[str(i)],)))
                i = i-1
                
        for repeat in range (0,2):  
            processes.append(multiprocessing.Process(target=on, args=(helper['3'],)))
            processes.append(multiprocessing.Process(target=on, args=(helper['2'],)))
            processes.append(multiprocessing.Process(target=on, args=(helper['4'],)))
            processes.append(multiprocessing.Process(target=on, args=(helper['1'],)))
            processes.append(multiprocessing.Process(target=on, args=(helper['5'],)))
            
            processes.append(multiprocessing.Process(target=off, args=(helper['5'],)))
            processes.append(multiprocessing.Process(target=off, args=(helper['1'],)))
            processes.append(multiprocessing.Process(target=off, args=(helper['4'],)))
            processes.append(multiprocessing.Process(target=off, args=(helper['2'],)))
            processes.append(multiprocessing.Process(target=off, args=(helper['3'],)))
        
        for repeat in range(0,5):
            processes.append(multiprocessing.Process(target=off, args=(helper['1'],)))
            
        for pin in range (1, 6):
            processes.append(multiprocessing.Process(target=on, args=(helper[str(pin)],)))
            for sleep in range (0,10):
                processes.append(multiprocessing.Process(target=off, args=(40,)))
                
        for pin in range (1, 6):
            processes.append(multiprocessing.Process(target=off, args=(helper[str(pin)],)))
        
                
        i = 0
        while i < len(processes):
            processes[i].start()
            if not parallel:
                processes[i].join()
            i += 1
        if parallel:
            i = 0
            while i < len(processes):
                processes[i].join()
                i += 1

        time.sleep(1.5)

    GPIO.cleanup()
