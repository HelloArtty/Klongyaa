from gpiozero import DistanceSensor
from time import sleep

# Initialize ultrasonic sensors
sensor1 = DistanceSensor(echo=3, trigger=2, max_distance=2.0)  # Max distance in meters
sensor2 = DistanceSensor(echo=15, trigger=14, max_distance=2.0)

def test_sensors():
    try:
        while True:
            # Measure distances
            distance1 = sensor1.distance * 100  # Convert to cm
            distance2 = sensor2.distance * 100  # Convert to cm

            print(f"Sensor 1 Distance: {distance1:.2f} cm")
            print(f"Sensor 2 Distance: {distance2:.2f} cm")
            print("-" * 30)

            sleep(1)  # Wait 1 second between readings

    except KeyboardInterrupt:
        print("Test interrupted by user.")

    finally:
        print("Test complete.")

# Run the test
test_sensors()
