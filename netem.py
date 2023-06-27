import os
import time
import csv
import sys

nic1 = sys.argv[1] #Download interface
nic2 = sys.argv[2] #Upload interface
length = int(sys.argv[3])
start = time.time()

os.system(f'sudo tc qdisc del dev {nic1} root')
os.system(f'sudo tc qdisc del dev {nic2} root')

# os.system(f'sudo tc qdisc add dev {nic} root handle 1: netem delay 15ms 1ms distribution normal')
# sudo tc qdisc add dev eth0 parent 1: handle 2: tbf rate 40mbit burst 160kbit limit 500kbit

while True:
    with open('B_2018.01.19_07.31.48.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            DL_bitrate = float(row[12])
            UL_bitrate = float(row[13])
            if line_count == 0:
                command_start = time.time()
                os.system(f'sudo tc qdisc add dev {nic1} root tbf rate {DL_bitrate}kbit burst 50kbit limit 500kbit')
                os.system(f'sudo tc qdisc show dev {nic1}')
                os.system(f'sudo tc qdisc add dev {nic2} root tbf rate {UL_bitrate}kbit burst 50kbit limit 500kbit') #apply >
                os.system(f'sudo tc qdisc show dev {nic2}') #show current traffic settings
                line_count +=1
                time.sleep(1- (time.time() - command_start))
                continue
            command_start = time.time()
            
            os.system(f'sudo tc qdisc change dev {nic1} root tbf rate {DL_bitrate}kbit burst 50kbit limit 500kbit') #apply traffic settings
            os.system(f'sudo tc qdisc show dev {nic1}') #show current traffic settings
            
            os.system(f'sudo tc qdisc change dev {nic2} root tbf rate {UL_bitrate}kbit burst 50kbit limit 500kbit') #apply traffic settings
            os.system(f'sudo tc qdisc show dev {nic2}') #show current traffic settings
            
            time.sleep(1 - (time.time() - command_start))
            now = time.time() 
            if (now - start) > length:
                print(now - start)
                print("stop")
                break
        if (now - start) > length:
            os.system(f'sudo tc qdisc del dev {nic1} root')
            os.system(f'sudo tc qdisc del dev {nic2} root')
            break
