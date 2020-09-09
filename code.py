import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_debouncer import Debouncer
from analogio import AnalogIn

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

def make_debouncable(pin):
    switch_io = DigitalInOut(pin)
    switch_io.direction = Direction.INPUT
    switch_io.pull = Pull.UP
    return switch_io

leds = [DigitalInOut(board.D22), DigitalInOut(board.D30),
    DigitalInOut(board.D36), DigitalInOut(board.D42),
    DigitalInOut(board.D48), DigitalInOut(board.D23),
    DigitalInOut(board.D31), DigitalInOut(board.D37)]


for led in leds:
    led.direction = Direction.OUTPUT

buttons = [Debouncer(make_debouncable(board.D26)), Debouncer(make_debouncable(board.D34)),
    Debouncer(make_debouncable(board.D40)), Debouncer(make_debouncable(board.D46)),
    Debouncer(make_debouncable(board.D52)), Debouncer(make_debouncable(board.D27)),
    Debouncer(make_debouncable(board.D29)), Debouncer(make_debouncable(board.D35))]

for button in buttons:
    button.direction = Direction.INPUT
    button.pull = Pull.UP

button_states = [False, False, False, False,
    False, False, False, False]

notes = [44, 46, 48, 50, 52, 54, 56, 58];

steps = [False, False, False, False,
    False, False, False, False]

current_step = 0
last_step = 7
last_time = 0.0

note_pots = [AnalogIn(board.A0), AnalogIn(board.A1), AnalogIn(board.A2), AnalogIn(board.A3),
    AnalogIn(board.A4), AnalogIn(board.A5), AnalogIn(board.A6), AnalogIn(board.A7)]

def note_for_value(value):
    note = value
    return note

tempo_pin = AnalogIn(board.A8)
step_length = 0.35

def translate(value, leftMin, leftMax, rightMin, rightMax):
    #find range width
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    #convert left range into a 0-1.0 float
    valueScaled = float(value - leftMin) / float(leftSpan)

    #convert left range float val into right range
    return rightMin + (valueScaled * rightSpan)


while True:

    #light steps
    for s in range(len(steps)):
        if steps[s] == True:
            leds[s].value = True
        else:
            leds[s].value = False

    #update buttons debounce
    for button in buttons:
        button.update()

    #check buttons
    for i in range(len(buttons)):
        button = buttons[i]
        if button.value == False:
            button_states[i] = True
        else:
            if button_states[i] == True:
                #button was just released, toggle step state
                steps[i] = not steps[i]
                button_states[i] = False

    #read note pots
    for p in range(len(note_pots)):
        val = int(translate(note_pots[p].value, 256, 65520, 22, 66))
        notes[p] = val

    #step through sequence steps
    now = time.monotonic()
    if now - last_time >= step_length:

        #pulse led for step
        leds[current_step].value = not steps[current_step]
        #find step length
        step_length = translate(tempo_pin.value, 256, 65520, 1.0, 0.01)
        last_time = now
        midi.send(NoteOff(notes[last_step], 120))
        if steps[current_step] == True:
            midi.send(NoteOn(notes[current_step], 120))

        #increment step
        last_step = current_step
        current_step += 1
        if current_step > 7:
            current_step = 0

    #pad loop
    time.sleep(0.01)