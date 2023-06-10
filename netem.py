import os
import time
import csv
import sys

nic = sys.argv[1]

os.system(f'sudo tc qdisc del dev {nic} root')
os.system(f'sudo tc qdisc add dev {nic} root handle 1: netem delay 15ms 1ms distribution normal')

while True:
    with open('B_2018.01.19_07.31.48.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            #skip the first row of csv file
            if line_count == 0:
                line_count += 1
                continue
            DL_bitrate = float(row[12])*0.001 #convert kbit/s to mbit/s
            #UL_bitrate = row[13]
            if line_count == 1:
                os.system(f'sudo tc qdisc add dev {nic} parent 1: handle 2: tbf rate {DL_bitrate}mbit burst 160kbit limit 500kbit')
                os.system(f'sudo tc qdisc show dev {nic}')
                line_count += 1
                time.sleep(1)
                continue
            os.system(f'sudo tc qdisc change dev {nic} parent 1: handle 2: tbf rate {DL_bitrate}mbit burst 160kbit limit 500kbit') #apply traffic settings
            os.system(f'sudo tc qdisc show dev {nic}') #show current traffic settings
            time.sleep(1) #delay for 1s