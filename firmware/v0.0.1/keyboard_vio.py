import keynames
import keyboard_phyio

from adafruit_hid.keyboard import Keyboard
import os

class KeyboardVirtualIO():
    phy_io: keyboard_phyio.KeyboardPhyIO
    status: keyboard_phyio.KeyboardStatus

    def __init__(self, phy_io: keyboard_phyio.KeyboardPhyIO, status: keyboard_phyio.KeyboardStatus):
        self.phy_io = phy_io
        self.status = status

class KeyboardLayer():
        layer_definition: dict = {}
        file_path: str = "<Invalid File Path>"
        file_name: str = "<Invalid File Name>"

        def __init__(self, file_path: str):
            # Open file path    ok
            # read file         ok
            # parse file
            # get layer definition from parser

            self._load_layer(file_path)

        def _load_layer(self, file_path: str):
            self.file_path = file_path
            self.file_name = self._get_file_name(file_path)
            contents = self._get_file_contents(file_path)
            
            fc = self._parse_file_contents(contents)
            self.layer_definition = {
                "META":{
                    "name": self.file_name,
                    "file_path": self.file_path
                },
                "def": fc
            }
        
        def _get_file_name(self, file_path: str):
            ret = file_path.split(os.sep)[-1]
            ret = ret.replace("_keymap.txt", "")
            return ret

        def _get_file_contents(self, file_path: str):
            with open(file_path, "r") as foo:
                contents = foo.readlines()
            return contents

        def _parse_file_contents(self, file_contents: list):
            layer_line_def: dict = {}
            
            line_number = 0
            for line in file_contents:
                line = line.strip()
                line_number += 1
                if line.startswith("#") or len(line) < 1 :
                    # print(f"Comment parsing @ {self.file_name} line {line_number}")
                    continue

                rk_action_split = line.split(":")
                if len(rk_action_split) < 2:
                    print(f"Error parsing @ {self.file_name} line {line_number}")
                    continue
                rk = rk_action_split[0].split(",")
                if len(rk) != 2:
                    print(f"Error parsing @ {self.file_name} line {line_number}")
                    continue
                rk = [k.strip() for k in rk]
                (r, k) = rk
                
                layer_line_def[(r, k)] = rk_action_split[1].strip()
            
            return layer_line_def


class KeyboardLayers():
    default: str = "base"
    __current_layer: str = ""
    loaded_layers_names: list = []
    loaded_layers: dict = {}

    def __init__(self):
        pass

    def get_rk_action(self, rk: tuple):
        action = ""
        if rk in self.loaded_layers[self.__current_layer]["def"]:
            action = self.loaded_layers[self.__current_layer]["def"][rk]
        return action

    def switch_layer_to(self, layer_name: str):
        if not layer_name in self.loaded_layers_names:
            print(f"error switching layers: {layer_name} not loaded")
        self.__current_layer = layer_name
    
    def print_curr_layer(self):
        print(self.loaded_layers[self.__current_layer])
        pass

    def load_all(self, folder_path: str):
        pass

    def load(self, file_path: str):
        print(f"loading {file_path}")
        tmp_layer = KeyboardLayer(file_path)
        layer_def = tmp_layer.layer_definition
        print(f"loaded new layer: " + layer_def["META"]["name"])
        self.loaded_layers[layer_def["META"]["name"]] = layer_def
        self.loaded_layers_names.append(layer_def["META"]["name"])
        
        return layer_def


class KeyboardAction():
    keynames: dict = {}
    kbd_layers: KeyboardLayers
    kbd_status: keyboard_phyio.KeyboardStatus

    kbd: Keyboard

    pressed_keys: dict = {}
    held_keys: dict = {}

    def __init__(self, layers: KeyboardLayers, status: keyboard_phyio.KeyboardPhyIO, kbd: Keyboard):
        self.keynames = keynames.KEYNAMES
        self.kbd_layers = layers
        self.kbd_status = status
        self.kbd = kbd

    def act_on_report(self):
        print(self.kbd_status.status_update)
        to_press = self.kbd_status.status_update["pressed"]
        to_release = self.kbd_status.status_update["released"]

        self._press_keys(to_press)
        self._release_keys(to_release)

    def _press_keys(self, to_press: list):
        for k in to_press:
            self._press_key(k)

    def _release_keys(self, to_release: list):
        for k in to_release:
            self._release_key(k)

    def _press_key(self, k):
        # get keymap
        action = self.kbd_layers.get_rk_action(k)
        keycode = self._get_keycode_from_keyname(action)
        if keycode:
            self.kbd.press(keycode)

    def _release_key(self, k):
        action = self.kbd_layers.get_rk_action(k)
        keycode = self._get_keycode_from_keyname(action)
        if keycode:
            self.kbd.release(keycode)

    def _hold_key(self):
        pass

    def _get_keycode_from_keyname(self, keyname):
        keycode = None
        if keyname in self.keynames:
            keycode = self.keynames[keyname]
        return keycode
