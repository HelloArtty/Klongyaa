from gpiozero import LED
from time import sleep

# Define the GPIO pins for the LEDs
led_pins = [4, 17, 27, 22, 23, 18, 24, 25]

# Initialize LED objects for each pin
leds = [LED(pin) for pin in led_pins]

def test_leds():
    try:
        # Turn each LED on and off sequentially
        for led, pin in zip(leds, led_pins):
            led.on()  # Turn on LED
            print(f"LED on GPIO {pin} ON")
            sleep(1)  # Wait for 1 second
            led.off()  # Turn off LED
            print(f"LED on GPIO {pin} OFF")
            sleep(1)  # Wait for 1 second

    except KeyboardInterrupt:
        print("Test interrupted by user.")

    finally:
        # Ensure all LEDs are off before exit
        for led in leds:
            led.off()
        print("Test complete. All LEDs off.")

# Run the LED test
test_leds()
