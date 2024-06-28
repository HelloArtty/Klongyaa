import RPi.GPIO as GPIO
import time
from gpiozero import LED
from hx711 import HX711

# ตั้งค่า GPIO โดยใช้การกำหนดหมายเลขแบบ BCM
GPIO.setmode(GPIO.BOARD)

# เริ่มต้นเซ็นเซอร์ HX711
# hx = HX711(dout_pin=31, pd_sck_pin=29)


# ฟังก์ชันสำหรับเริ่มต้นเซ็นเซอร์ HX711
def setup_hx711(hx):
    hx.reset()
    hx.set_scale_ratio(1)
    hx.set_offset(0)
    for _ in range(20):
        hx._read()




SCALE_BOX = 406189 / 10
# ฟังก์ชันสำหรับแปลงค่าเป็นกรัม
def to_grams(raw_value):
    return raw_value / SCALE_BOX

# ฟังก์ชันสำหรับรับค่าน้ำหนักเริ่มต้น
def get_first_load_value(dout_pin, pd_sck_pin):
    try:
        hx = HX711(dout_pin, pd_sck_pin)
        setup_hx711(hx)
        print("เริ่มต้น HX711 เรียบร้อยแล้ว")
        first_weight_raw = hx.get_raw_data_mean(25)
        if first_weight_raw is None:
            print("ไม่สามารถอ่านค่าได้")
            return -1
        else:
            first_weight_grams = to_grams(first_weight_raw)
            print(f"น้ำหนักเริ่มต้น: {first_weight_grams:.2f} กรัม")
            return first_weight_raw
    except Exception as e:
        print(f"เกิดข้อผิดพลาดใน get_first_load_value: {e}")
        return -1

# ฟังก์ชันสำหรับตรวจจับการหยิบยา
def pick_pill_detection(first_load_value,dout_pin,pd_sck_pin, led):
    led.on()
    try:
        hx = HX711(dout_pin, pd_sck_pin)
        setup_hx711(hx)
        current_weight_raw = hx.get_raw_data_mean(25)
        if current_weight_raw is None:
            print("ไม่สามารถอ่านค่าได้")
            return False
        
        current_weight_grams = to_grams(current_weight_raw)
        first_load_grams = to_grams(first_load_value)
        
        print(f"น้ำหนักปัจจุบัน: {current_weight_grams:.2f} กรัม, น้ำหนักเริ่มต้น: {first_load_grams:.2f} กรัม")
        
        if first_load_value == -1:
            print("กำลังตั้งค่าน้ำหนักเริ่มต้นใหม่")
            first_load_value = current_weight_raw
        else:
            weight_difference = abs(first_load_grams - current_weight_grams) 
            print(f"ความแตกต่างของน้ำหนัก: {weight_difference:.2f} กรัม")
            if weight_difference > 0.35:
                led.off()
                print("ตรวจพบการหยิบยา")
                return False
            else:
                led.on()
                print("ไม่มีการหยิบยา")
                return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาดใน pick_pill_detection: {e}")
        led.off()
        return False
    


'''
dt = 7
sck = 11
first_load_value = get_first_load_value(dt,sck)



while True:
    result = pick_pill_detection(first_load_value,dt,sck)
    time.sleep(1)  #fv'''
