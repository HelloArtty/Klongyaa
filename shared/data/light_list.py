import RPi.GPIO as GPIO
from gpiozero import LED


lightList = {
    "0": {
        "dout":8,
        "pdPin":10,
        "led": LED(23),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "1": {
        "dout":3,
        "pdPin":5,
        "led": LED(24),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "2": {
        "dout":7,
        "pdPin":11,
        "led": LED(25),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "3": {
        "dout":13,
        "pdPin":15,
        "led": LED(8),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "4": {
        "dout":19,
        "pdPin":21,
        "led": LED(7),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "5": {
        "dout":23,
        "pdPin":27,
        "led": LED(1),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "6": {
        "dout":29,
        "pdPin":31,
        "led": LED(12),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "7": {
        "dout":33,
        "pdPin":35,
        "led": LED(16),
        "haveToTake": False,
        "firstWeightValue": -1
    },
}