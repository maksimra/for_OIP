import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

dac = [8,11,7,1,0,5,12,6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN, )

def dec2bin(value):
    return [int(el) for el in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    num = 0
    for bit in range(7, -1, -1):
        num += 2**bit
        num2dac(num)
        time.sleep(0.005)
        compVal = GPIO.input(comp)
        if compVal == 1:
            num -= 2**bit
    return num

data_volts = []
data_times = []

GPIO.output(troyka, 1)

start_time = time.time()

val = 0

try:
    while(val < 205):
        val = adc()
        volt = float(val)/256*3.3
        print("ADC: val = {}, input volt = {:.2f}".format(num2dac(val), volt))
        data_volts.append(val)
        data_times.append(time.time()- start_time)

    GPIO.output(troyka, 0)

    while(val > 170):
        val = adc()
        volt = float(val)/256*3.3
        print("ADC: val = {}, input volt = {:.2f}".format(num2dac(val), volt))
        data_volts.append(val)
        data_times.append(time.time()- start_time)

    end_time = time.time()
    
    with open("./settings.txt", "w") as file:
        file.write(str((end_time - start_time)/len(data_volts)))
        file.write("\n")
        file.write(str(3.3/256))
    data_times_str = [str(i) for i in data_times]
    data_volts_str = [str(i) for i in data_volts]
    with open("data.txt", "w") as file:
        file.write("\n".join(data_volts_str))
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()
    print("END")

_, ax = plt.subplots(figsize=(14, 10))
ax.set_xlabel("t, с", fontweight="bold")
ax.set_ylabel("U, В", fontweight="bold")
ax.set_title("График U(t)", fontweight="bold")

my_plot = plt.plot(data_times, data_volts,12)

plt.grid()  #just add this

plt.plot(data_times, data_volts)
plt.show()