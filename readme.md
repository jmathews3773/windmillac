# Custom Component for Windmill AC Integration in Home Assistant

The Windmill AC platform allows you to control a Windmill AC climate entity.

There is currently support for the following device types within Home Assistant:

-   Climate

## Installation

1. Download the latest release from: https://github.com/jmathews3773/windmillac/releases
2. Extract the file
3. Copy the whole **windmillac-homeassistant** folder from **custom_components/** to your own **config/custom_components/** directory
4. Go to Config -> Server Controls -> Under "Server Management" click restart
5. Go to configuration example for how to set up your config.

Alternatively, you can install through [HACS](https://hacs.xyz) by adding this repository.


# Climate Configuration 

### Example of basic configuration.yaml
```
climate:
  - platform: windmillac
    name: bedroom_ac
    access_token: <YOUR_WINDMILL_TOKEN>
```