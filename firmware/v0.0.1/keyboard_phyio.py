from digitalio import DigitalInOut, Direction, Pull


class KeyboardPhyIO():
    phy_rows: dict = {}
    phy_cols: dict = {}
    rows: dict = {}
    cols: dict = {}

    def __init__(self, PHY_DEF):
        self.phy_rows = PHY_DEF["rows"]
        self.phy_cols = PHY_DEF["cols"]
        # self.setup()

    def setup(self):
        self._setup_rows()
        self._setup_cols()

    def _setup_rows(self):
        for pin_name in self.phy_rows:
            pin = self.phy_rows[pin_name]
            key_pin = DigitalInOut(pin)
            key_pin.direction = Direction.OUTPUT
            self.rows[pin_name] = key_pin

    def _setup_cols(self):
        for pin_name in self.phy_cols:
            pin = self.phy_cols[pin_name]
            key_pin = DigitalInOut(pin)
            key_pin.direction = Direction.INPUT
            key_pin.pull = Pull.DOWN
            self.cols[pin_name] = key_pin


class KeyboardStatus():
    kb_phyio: KeyboardPhyIO

    curr_status: list = []
    last_status: list = []
    status_update: dict = {}

    def __init__(self, kb_phyio: KeyboardPhyIO):
        self.kb_phyio = kb_phyio

    def scan_diff(self):
        self._scan_keys()
        self._get_keys_diff()
        return self.status_update
    
    def get_if_update(self):
        return (self.status_update["pressed"] != [] or self.status_update["released"] != [])
    
    def print_if_update(self):
        if self.status_update["pressed"] != [] or self.status_update["released"] != []:
            print(self.status_update)

    def _scan_keys(self):
        self.last_status = self.curr_status
        pressed_keys_arr = []

        for row_pin_name in self.kb_phyio.rows:
            row_pin = self.kb_phyio.rows[row_pin_name]
            row_pin.value = True
            for col_pin_name in self.kb_phyio.cols:
                col_pin = self.kb_phyio.cols[col_pin_name]
                if col_pin.value:
                    pressed_keys_arr.append((row_pin_name, col_pin_name))
            row_pin.value = False
        self.curr_status = pressed_keys_arr
    
    def _get_keys_diff(self):
        pressed_arr = []
        released_arr = []
        if not self.last_status is None:
            for rk in self.last_status:
                if not rk in self.curr_status:
                    released_arr.append(rk)

            for rk in self.curr_status:
                if not rk in self.last_status:
                    pressed_arr.append(rk)

        ret_arr = {
            "pressed": pressed_arr,
            "released": released_arr
        }
        self.status_update = ret_arr
    
    