# import random
# import time


# # จำลอง GPIO
# class MockGPIO:
#     BCM = 'BCM'
    
#     @staticmethod
#     def setmode(mode):
#         print(f"Setting mode: {mode}")
    
#     @staticmethod
#     def setup(pin, mode):
#         print(f"Setting up pin {pin} as {mode}")
    
#     @staticmethod
#     def output(pin, value):
#         print(f"Setting pin {pin} to {value}")
    
#     @staticmethod
#     def input(pin):
#         # จำลองการวัดระยะจากเซ็นเซอร์
#         return random.choice([0, 1])

# # ใช้ MockGPIO แทน RPi.GPIO
# GPIO = MockGPIO

# # จำลองเซ็นเซอร์วัดระยะทาง
# class DistanceSensor:
#     def __init__(self, echo, trig):
#         self.echo = echo
#         self.trig = trig
    
#     @property
#     def distance(self):
#         # จำลองการคืนค่าระยะทางแบบสุ่ม
#         return random.uniform(5, 30)

# # จำลอง LED
# class MockLED:
#     def off(self):
#         print("LED off")

# # ตั้งค่า GPIO แบบ BCM
# GPIO.setmode(GPIO.BCM)

# def setup_ultrasonic(trig, echo):
#     GPIO.setup(trig, "OUT")
#     GPIO.setup(echo, "IN")

# def detect_pill_removal(sensor_1, sensor_2, led, box_index):
#     print(box_index)

#     distance_1 = sensor_1.distance
#     distance_2 = sensor_2.distance
#     print(f"Distance 1: {distance_1:.2f} cm, Distance 2: {distance_2:.2f} cm")

#     # ใช้ระยะที่วัดได้จากทั้งสองเซ็นเซอร์เพื่อตรวจจับว่ามีการหยิบยาจากช่องไหน
#     if box_index == 1 or box_index == 0:
#         if 21 < distance_1 <= 28 or 21 < distance_2 <= 28:
#             print("Pill from slot 1 is being taken")
#             led.off()
#         return False
#     if box_index == 3 or box_index == 2:
#         if 14 < distance_1 <= 21 or 14 < distance_2 <= 21:
#             print("Pill from slot 3 is being taken")
#             led.off()
#         return False
#     if box_index == 5 or box_index == 4:
#         if 7 < distance_1 <= 14 or 7 < distance_2 <= 14:
#             print("Pill from slot 5 is being taken")
#             led.off()
#         return False
#     if box_index == 7 or box_index == 6:
#         if distance_1 <= 7 or distance_2 <= 7:
#             print("Pill from slot 7 is being taken")
#             led.off()
#         return False
#     return True

# # จำลองเซ็นเซอร์และ LED
# sensor_1 = DistanceSensor(2, 3)
# sensor_2 = DistanceSensor(4, 5)
# led = MockLED()

# # ทดลองการตรวจจับการหยิบยา
# detect_pill_removal(sensor_1, sensor_2, led, 1)
