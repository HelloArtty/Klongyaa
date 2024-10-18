from gpiozero import DistanceSensor, LED
from time import sleep

# ฟังก์ชันสำหรับตรวจจับการหยิบยาโดยใช้เซ็นเซอร์สองตัว
def detect_pill_removal(sensor_1, sensor_2, led):
    # วัดระยะจากเซ็นเซอร์ตัวที่ 1 และตัวที่ 2
    distance_1 = sensor_1.distance * 100  # ระยะทางในเซนติเมตร
    distance_2 = sensor_2.distance * 100  # ระยะทางในเซนติเมตร
    
    print(f"Distance 1: {distance_1:.2f} cm, Distance 2: {distance_2:.2f} cm")

    # ใช้ระยะที่วัดได้จากทั้งสองเซ็นเซอร์เพื่อตรวจจับว่ามีการหยิบยาจากช่องไหน
    if distance_1 <= 7 or distance_2 <= 7:
        print("Pill from slot 7 is being taken")
        led.off()
        return 7
    elif 7 < distance_1 <= 14 or 7 < distance_2 <= 14:
        print("Pill from slot 5 is being taken")
        led.off()
        return 5
    elif 14 < distance_1 <= 21 or 14 < distance_2 <= 21:
        print("Pill from slot 3 is being taken")
        led.off()
        return 3
    elif 21 < distance_1 <= 28 or 21 < distance_2 <= 28:
        print("Pill from slot 1 is being taken")
        led.off()
        return 1
    else:
        print("No pill is being taken")
        led.on()
        return None

# ตัวอย่างการใช้งาน
if __name__ == "__main__":

    sensor_1 = DistanceSensor(echo=3, trigger=2)   
    sensor_2 = DistanceSensor(echo=15, trigger=14) 
    led = LED(23)  # พินที่ใช้ควบคุม LED

    # เริ่มต้นเปิด LED เพื่อแสดงว่าไม่มีการหยิบยา
    led.on()

    try:
        while True:
            pill_slot = detect_pill_removal(sensor_1, sensor_2, led)
            if pill_slot is not None:
                print(f"Pill taken from slot {pill_slot}")
            sleep(1)

    except KeyboardInterrupt:
        print("Program stopped")
