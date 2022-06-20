import SCO67_DEF

import keyboard_vio
import keyboard_phyio
from keynames import KEYNAMES

import usb_hid
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

LOOP_INTERVAL = 0.5 
PHY_DEF = SCO67_DEF.SCO67_PHY_DEF

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

kbd_io: keyboard_phyio.KeyboardPhyIO
kbd_vio: keyboard_vio.KeyboardVirtualIO
kbd_status: keyboard_phyio.KeyboardStatus
kbd_layers: keyboard_vio.KeyboardLayers
kbd_action: keyboard_vio.KeyboardAction

kbd_io = keyboard_phyio.KeyboardPhyIO(PHY_DEF)
kbd_io.setup()
kbd_status = keyboard_phyio.KeyboardStatus(kbd_io)
kbd_vio = keyboard_vio.KeyboardVirtualIO(kbd_io, kbd_status)

kbd_layers = keyboard_vio.KeyboardLayers()
kbd_layers.load("/keymap/base_keymap.txt")
kbd_layers.load("/keymap/layer2_keymap.txt")
kbd_layers.switch_layer_to("base")

kbd_action = keyboard_vio.KeyboardAction(kbd_layers, kbd_status, keyboard)

while 1:
    update = kbd_status.scan_diff()
    # kbd_status.print_if_update()
    if kbd_status.get_if_update():
        kbd_action.act_on_report()

    time.sleep(LOOP_INTERVAL)