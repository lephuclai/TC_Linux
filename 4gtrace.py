import os
import time
import csv

while True:
    with open('B_2018.01.19_07.31.48.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            DL_bitrate = float(row[12])*0.001 
            #UL_bitrate = row[13]
            os.system(f'sudo tc qdisc add dev ens33 root tbf rate {DL_bitrate}mbit burst 32kbit latency 400ms')
            os.system(f'sudo tc qdisc show dev ens33')
            time.sleep(1)
            os.system(f'sudo tc qdisc del dev ens33 root')
            line_count += 1