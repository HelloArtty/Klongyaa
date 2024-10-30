# จำลอง GPIO
class MockGPIO:
    BCM = 'BCM'
    
    @staticmethod
    def setmode(mode):
        print(f"Setting mode: {mode}")
    
    @staticmethod
    def setup(pin, mode):
        print(f"Setting up pin {pin} as {mode}")
    
    @staticmethod
    def output(pin, value):
        print(f"Setting pin {pin} to {value}")
    
    @staticmethod
    def input(pin):
        return 0  # จำลองค่าอินพุต

# จำลอง LED
class MockLED:
    def __init__(self, pin):
        self.pin = pin
    
    def on(self):
        print(f"LED on pin {self.pin} is ON")
    
    def off(self):
        print(f"LED on pin {self.pin} is OFF")

# ใช้ MockGPIO แทน RPi.GPIO
GPIO = MockGPIO

# สร้าง lightList โดยใช้ MockLED และเพิ่มพินสำหรับ ultrasonic sensor
lightList = {
    "0": {
        "trigPin_1": 17,
        "echoPin_1": 27,
        "trigPin_2": 22,
        "echoPin_2": 23,
        "led": MockLED(23),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "1": {
        "trigPin_1": 5,
        "echoPin_1": 6,
        "trigPin_2": 13,
        "echoPin_2": 19,
        "led": MockLED(24),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "2": {
        "trigPin_1": 21,
        "echoPin_1": 20,
        "trigPin_2": 16,
        "echoPin_2": 12,
        "led": MockLED(25),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    "3": {
        "trigPin_1": 25,
        "echoPin_1": 8,
        "trigPin_2": 7,
        "echoPin_2": 1,
        "led": MockLED(8),
        "haveToTake": False,
        "firstWeightValue": -1
    },
    # สามารถเพิ่มค่าได้ตามที่ต้องการสำหรับช่องอื่นๆ
}

# ทดสอบการเปิดปิด LED ใน lightList
for index, light in lightList.items():
    print(f"Testing LED for light {index}")
    light["led"].on()
    light["led"].off()
