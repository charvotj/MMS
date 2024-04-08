import smbus
import math
import kADXL345 as ad

def main():
    bus = smbus.SMBus(1)
    ad.Inicializace345(bus, 0x1E, 0x20)

    print("deg\trot\tnak")
    deg=0
    # vlozeni breakpointu na zacatek cyklu umozni jednoduche krokovani pri nastaveni uhlu 
    while True:
        x = ad.Precteni(bus, 0x32, 0x33)
        y = ad.Precteni(bus, 0x34, 0x35)
        z = ad.Precteni(bus, 0x36, 0x37)
        if (x == 0) and ( z==0 ) or (y == 0) and (z ==0):
            pass
        else:
            rot = 0
            nak = 0
            for deg in range(0, 10):
                rot += math.atan(y/math.sqrt(math.pow(x, 2) + math.pow(z, 2))) * 180/math.pi
                nak += math.atan(-1 * x/math.sqrt(math.pow(y, 2) + math.pow(z, 2))) * 180/math.pi
            rot = format(rot, '.4f')
            nak = format(nak, '.4f')
            print(str(deg) + '\t' + str(rot) + '\t' + str(nak) + '\n')
            deg += 10

if __name__ == "__main__":
    main()