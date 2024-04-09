from ADCPi import ADCPi 
from time import sleep 

adc = ADCPi(0x68, 0x69, 18) 
print('Kalibruji...') 
mV_offset = 0 
for i in range(100): 
    mV_offset += adc.read_voltage(1)*1000 
    sleep(0.1) 
    if(i % 10 == 0): 
        print(i/10) 
mV_offset /=100 
print(f'{mV_offset:.02f} mV') 
sens = 0.3 
coef_actn = 1.2 
adc.read_voltage(1)*1000 

while True: 
    ppm = 0 
    for i in range(10): 
        ppm += (((adc.read_voltage(1)*1000)-mV_offset)/sens *coef_actn) 
        sleep(0.1) 
        print(f'{ppm/10.0:.02f1} ppm') 
    sleep(1) 

