import os
import time
import csv
import sys

nic = sys.argv[1]

os.system(f'sudo tc qdisc del dev {nic} root')
# os.system(f'sudo tc qdisc add dev {nic} root handle 1: netem delay 15ms 1ms distribution normal')
# sudo tc qdisc add dev eth0 parent 1: handle 2: tbf rate 40mbit burst 160kbit limit 500kbit


while True:
    with open('B_2018.01.19_07.31.48.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            #skip the first row of csv file
            # if line_count == 0:
            #     line_count += 1
            #     continue
            DL_bitrate = float(row[12])*0.001 #convert kbit/s to mbit/s
            burst = ((DL_bitrate * 1000000)/250)/1000

            #UL_bitrate = loat(row[13])*0.001
            # if line_count == 0:
            #     os.system(f'sudo tc qdisc add dev {nic} root handle 1: tbf rate {DL_bitrate}mbit burst 160kbit limit 500kbit')
            #     os.system(f'sudo tc qdisc show dev {nic}')
            #     line_count += 1
            #     time.sleep(1)
            #     continue

            os.system(f'sudo tc qdisc add dev {nic} root handle 1: tbf rate {DL_bitrate}mbit burst {burst}kbit limit 5000kbit') #apply traffic settings
            os.system(f'sudo tc qdisc show dev {nic}') #show current traffic settings
            os.system(f'sudo tc qdisc del dev {nic} root')
            time.sleep(1) #delay for 1s