# SCO67


## For action
### Hardware
Main: <br>
- SW61 is not connected -> Solder jumper from D50 to D61
- D41 & D65 (COL 14) not connected (not accounted for) -> Solder new connection to carrier board.
- Capslock (SW29) is out of place.

Daughter Board: <br>
- Connections on WEACT PI PICO RP2040 is incorrectly reflected to headers in kicad

### Software
- microcontroller does not start immediately on boot. 
    - reviewed and solved temporarly by mounting device in boot.py
- Found limitation that there is max 6kro (6 Key Roll Over) not NKRO!!


Layers are not implemented fully
Multikey actions are not implemented fully
