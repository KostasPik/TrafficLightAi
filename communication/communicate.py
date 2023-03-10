import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=1, write_timeout=1)

arduino.reset_output_buffer()
arduino.reset_input_buffer()

while 1:
    var = str(input("Input:"))
    arduino.write(bytes(var, 'utf-8'))
    time.sleep(1)
    print("ARDUINO SAYS:", arduino.readline().strip().decode('ascii'))
    arduino.flush()
