from datetime import datetime
import time
import os
import random
import logging

INTERVAL_BETWEEN_ATTACKS = 20  # seconds
MINIMUM_PACKET_LOSS_PERCENTAGE = 20

if __name__ == '__main__':
    logging.basicConfig(filename='antagonist.log', level=logging.INFO)  # open in append mode
    logging.info("%s - Antagonist started\n"
                 "Interval between change of packet loss threshold: %d", datetime.now(), INTERVAL_BETWEEN_ATTACKS)

    while 1:
        os.system("tc qdisc del dev eth0 root")  # remove the old rule
        # adding a packet loss percentage
        packet_loss_percentage = random.randint(MINIMUM_PACKET_LOSS_PERCENTAGE, 100)  # percentage of packet loss
        os.system("tc qdisc add dev eth0 root netem loss " + str(packet_loss_percentage) + "%")
        logging.info("%s - Packet loss percentage: %d%%", datetime.now(), packet_loss_percentage)
        time.sleep(INTERVAL_BETWEEN_ATTACKS)
