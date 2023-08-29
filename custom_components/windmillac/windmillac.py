import requests
import logging

from custom_components.windmillac.const import CURRENT_TEMP, TARGET_TEMP, MODE, FAN, POWER, POWER_ON, POWER_OFF

_LOGGER = logging.getLogger(__name__)

BASE_URI = "https://dashboard.windmillair.com/external/api/"
GET_SUFFIX = "get"
UPDATE_SUFFIX = "update"


class WindmillAC:

    def __init__(self, token: str):
        self.token = token

    def get_current_temp(self) -> float:
        return float(self.__get_value(CURRENT_TEMP))

    def get_target_temp(self) -> float:
        return float(self.__get_value(TARGET_TEMP))

    def get_mode(self) -> str:
        return self.__get_value(MODE)

    def get_fan_speed(self):
        return self.__get_value(FAN)

    def set_target_temp(self, target: float):
        self.__update_value(TARGET_TEMP, target)

    def set_fan_speed(self, value: str):
        self.__update_value(FAN, value)

    def turn_on(self):
        self.__update_value(POWER, POWER_ON)

    def turn_off(self):
        self.__update_value(POWER, POWER_OFF)

    def is_on(self) -> bool:
        power = self.__get_value(POWER)
        if self.__get_value(POWER) == str(POWER_ON):
            return True
        return False

    def __get_value(self, pin: str) -> str:
        uri = BASE_URI + GET_SUFFIX + "?token=%s&%s=''" % (self.token, pin)
        r = requests.get(uri)
        return r.text

    def __update_value(self, pin: str, value: str) -> str:
        r = requests.get(BASE_URI + UPDATE_SUFFIX + "?token=%s&%s=%s" % (self.token, pin, value))
        return r.text