import os
import time
import csv

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
            os.system(f'sudo tc qdisc add dev ens33 root tbf rate {DL_bitrate}mbit burst 32kbit latency 400ms') #apply traffic settings
            os.system(f'sudo tc qdisc show dev ens33') #show current traffic settings
            time.sleep(1) #delay for 1s
            os.system(f'sudo tc qdisc del dev ens33 root') #delete traffic settings