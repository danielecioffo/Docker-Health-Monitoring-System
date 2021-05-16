import os
import docker
import random
import logging
from datetime import datetime
import time

NAME_OF_ANTAGONIST_CONTAINER = "antagonist"
NAME_OF_AGENT_CONTAINER = "agent"
INTERVAL_BETWEEN_ATTACKS = 20  # seconds
MINIMUM_PACKET_LOSS_PERCENTAGE = 40


def periodic_attack():
    list_of_containers = client.containers.list()  # get the active containers
    list_of_containers.remove(client.containers.get(NAME_OF_ANTAGONIST_CONTAINER))  # remove myself from the list
    if len(list_of_containers) != 0:  # if there are others containers active
        # FIRST ATTACK - STOP ONE CONTAINER
        index = random.randrange(len(list_of_containers))  # random value from 0 to length (of the list of containers)
        container_to_stop = list_of_containers[index]
        # stop the chosen container
        if container_to_stop.name != NAME_OF_AGENT_CONTAINER:  # do not consider the agent in attacks
            logging.info("%s - Container stopped: %s\n", datetime.now(), container_to_stop.name)
            container_to_stop.stop()

        # SECOND ATTACK - NETWORK PROBLEM
        os.system("tc qdisc del dev eth0 root")  # remove the old rule
        # adding a packet loss percentage
        packet_loss_percentage = random.randint(MINIMUM_PACKET_LOSS_PERCENTAGE, 100)  # percentage of packet loss
        os.system("tc qdisc add dev eth0 root netem loss " + str(packet_loss_percentage) + "%")
        logging.info("%s - Packet loss percentage: %d", datetime.now(), packet_loss_percentage)


if __name__ == '__main__':
    # open in write mode, to remove the old information logged
    logging.basicConfig(filename='execution.log', level=logging.INFO, filemode='w')
    logging.info("%s - Antagonist started\n"
                 "Interval between periodic checks: %d\n", datetime.now(), INTERVAL_BETWEEN_ATTACKS)

    # Instantiate the Docker client
    client = docker.from_env()
    while 1:
        periodic_attack()
        time.sleep(INTERVAL_BETWEEN_ATTACKS)