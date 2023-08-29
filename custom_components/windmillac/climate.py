from __future__ import annotations

from homeassistant.components.climate import ClimateEntity, HVACMode, ClimateEntityFeature, PLATFORM_SCHEMA, HVACAction
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE, CONF_ACCESS_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from custom_components.windmillac.const import FAN_AUTO, FAN_LOW, FAN_HIGH, FAN_MEDIUM, MODE_COOL, MODE_ECO, MODE_FAN
from custom_components.windmillac.windmillac import WindmillAC
import logging
from homeassistant.const import (
    CONF_NAME,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Required(CONF_NAME): cv.string
    }
)


def setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    _LOGGER.warning("Connecting to windmill_ac")
    windmill_ac = WindmillClimateEntity(
        config[CONF_ACCESS_TOKEN],
        config[CONF_NAME])
    add_entities([windmill_ac])


class WindmillClimateEntity(ClimateEntity):
    # Implement one of these methods.

    def __init__(self, token: str, name: str):
        self.windmill = WindmillAC(token)
        self._attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
        self._attr_hvac_modes = [HVACMode.OFF, HVACMode.COOL]
        self._attr_supported_features = self._get_supported_features()
        self._attr_fan_modes = ["FAN_AUTO", "FAN_LOW", "FAN_MEDIUM", "FAN_HIGH"]
        self._attr_fan_mode = "FAN_AUTO"
        self._name = name
        self._current_temp = None
        self._target_temp = None
        self._is_on = None
        self._mode = None

    @property
    def fan_modes(self):
        return ["FAN_AUTO", "FAN_LOW", "FAN_MEDIUM", "FAN_HIGH"]

    @staticmethod
    def _get_supported_features():
        features = ClimateEntityFeature(0)
        features |= ClimateEntityFeature.TARGET_TEMPERATURE
        features |= ClimateEntityFeature.FAN_MODE
        return features

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        return self._target_temp

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current operation (e.g. heat, cool, idle)."""
        if not self._is_on:
            return HVACMode.OFF
        if self._mode == MODE_COOL:
            return HVACMode.COOL
        elif self._mode == MODE_FAN:
            return HVACMode.FAN_ONLY
        else:
            return HVACMode.AUTO

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return self._current_temp

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action (cooling, idle, off)."""
        if not self._is_on:
            return HVACAction.OFF
        if self._mode == MODE_COOL:
            return HVACAction.COOLING
        elif self._mode == MODE_FAN:
            return HVACAction.FAN
        else:
            return HVACAction.IDLE

    def set_hvac_mode(self, hvac_mode: HVACMode):
        if hvac_mode not in self._attr_hvac_modes:
            raise NotImplementedError("Mode %s not implemented" % hvac_mode)
        if hvac_mode == HVACMode.OFF:
            self.windmill.turn_off()
        elif hvac_mode == HVACMode.COOL:
            self.windmill.turn_on()
        else:
            raise NotImplementedError("Mode %s not implemented" % hvac_mode)

    def set_fan_mode(self, fan_mode: str):
        if fan_mode == "FAN_AUTO":
            self.windmill.set_fan_speed(FAN_AUTO)
        elif fan_mode == "FAN_LOW":
            self.windmill.set_fan_speed(FAN_LOW)
        elif fan_mode == "FAN_MEDIUM":
            self.windmill.set_fan_speed(FAN_MEDIUM)
        elif fan_mode == "FAN_HIGH":
            self.windmill.set_fan_speed(FAN_HIGH)
        else:
            raise NotImplementedError("Fan mode %s not implemented" % fan_mode)

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        return self.windmill.set_target_temp(temp)

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._current_temp = self.windmill.get_current_temp()
        self._target_temp = self.windmill.get_target_temp()
        self._is_on = self.windmill.is_on()
        self._mode = self.windmill.get_mode()