import RPi.GPIO as GPIO
import time

# ตั้งค่า GPIO แบบ BCM
GPIO.setmode(GPIO.BCM)

# ฟังก์ชันสำหรับการตั้งค่าเซ็นเซอร์ Ultrasonic
def setup_ultrasonic(trig, echo):
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

# ฟังก์ชันสำหรับการวัดระยะทางจาก Ultrasonic Sensor
def get_distance(trig, echo):
    # ส่งสัญญาณ 10us pulse ไปที่พิน Trig
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    # วัดเวลาที่คลื่นเสียงใช้ไปกลับระหว่างเซ็นเซอร์กับสิ่งกีดขวาง
    while GPIO.input(echo) == 0:
        start_time = time.time()
    while GPIO.input(echo) == 1:
        end_time = time.time()

    # คำนวณระยะทางจากเวลาที่วัดได้
    time_elapsed = end_time - start_time
    distance = (time_elapsed * 34300) / 2  # คำนวณระยะทาง (เซนติเมตร)

    return distance

# ฟังก์ชันสำหรับตรวจจับการหยิบยาโดยใช้เซ็นเซอร์สองตัว
def detect_pill_removal(trig_1, echo_1, trig_2, echo_2, led):
    distance_1 = get_distance(trig_1, echo_1)
    distance_2 = get_distance(trig_2, echo_2)
    
    print(f"Distance 1: {distance_1:.2f} cm, Distance 2: {distance_2:.2f} cm")

    # ใช้ระยะของทั้งสองเซ็นเซอร์เพื่อตรวจสอบการหยิบยา
    if distance_1 <= 7 or distance_2 <= 7:
        print("Pill from slot 7 is being taken")
        led.off()
        return 7
    elif (7 < distance_1 <= 14 or 7 < distance_2 <= 14):
        print("Pill from slot 5 is being taken")
        led.off()
        return 5
    elif (14 < distance_1 <= 21 or 14 < distance_2 <= 21):
        print("Pill from slot 3 is being taken")
        led.off()
        return 3
    elif (21 < distance_1 <= 28 or 21 < distance_2 <= 28):
        print("Pill from slot 1 is being taken")
        led.off()
        return 1
    else:
        print("No pill is being taken")
        led.on()
        return None
