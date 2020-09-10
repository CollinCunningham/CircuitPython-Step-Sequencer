# CircuitPython Step Sequencer

8-step MIDI sequencer for [Adafruit Grand Central M4](https://www.adafruit.com/product/4084)

Assumes hardware connections:
- step LEDs: `D22, D30, D36, D42, D48, D23, D31, D37`
- step buttons: `D26, D34, D40, D46, D52, D27, D29, D35`
- step pots: `A0, A1, A2, .A3, A4, A5, A6, A7`
- tempo pot: `A8`

Known Issues
---
- Intermittent variance in step duration
- some missing noteOffs after note value changes
