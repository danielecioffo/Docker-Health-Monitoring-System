import docker
from random import randrange
import logging
from datetime import datetime
import time

NAME_OF_ANTAGONIST_CONTAINER = "antagonist"
INTERVAL_BETWEEN_ATTACKS = 5  # seconds


def periodic_attack():
    list_of_containers = client.containers.list()  # get the active containers
    list_of_containers.remove(client.containers.get(NAME_OF_ANTAGONIST_CONTAINER))  # remove myself from the list
    if len(list_of_containers) != 0:  # if there are others containers active
        index = randrange(len(list_of_containers))  # random value from 0 to length (of the list of containers)
        # stop the chosen container
        logging.info("%s - Container stopped: %s\n", datetime.now(), list_of_containers[index].name)
        list_of_containers[index].stop()


if __name__ == '__main__':
    # open in write mode, to remove the old information logged
    logging.basicConfig(filename='execution.log', level=logging.INFO, filemode='w')
    logging.info("%s - Antagonist started\n"
                 "Interval between periodic checks: %d\n", datetime.now(), INTERVAL_BETWEEN_ATTACKS)

    # Instantiate the Docker client
    client = docker.from_env()
    while 1:
        logging.info("%s - I'm performing an attack...", datetime.now())
        periodic_attack()
        time.sleep(INTERVAL_BETWEEN_ATTACKS)
