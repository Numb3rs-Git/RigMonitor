# Watchdog

Watchdog timer and sensor viewer.

An arduino listens for a heartbeat and sends sensor data from a DHT11 over serial to the desktop application.
If the arduino doesn't receive a heartbeat for 5 seconds, the computer is restarted.

The desktop application sends the heartbeat and displays the sensor data sent by the arduino.

Required software:
- Arduino IDE
- Python 3
- PyInstaller