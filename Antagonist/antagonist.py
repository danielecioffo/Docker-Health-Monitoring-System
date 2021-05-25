import docker
import random
import logging
from datetime import datetime
import time

INTERVAL_BETWEEN_ATTACKS = 30  # seconds

CONTAINERS_TO_AVOID = [
    "antagonist",
    "rabbitMq-broker",
    "swagger_server"
]


def periodic_attack():
    list_of_containers = client.containers.list()  # get the active containers
    for name in CONTAINERS_TO_AVOID:
        try:
            list_of_containers.remove(client.containers.get(name))
        except:
            pass
    if len(list_of_containers) != 0:  # if there are others containers active
        # STOP ONE CONTAINER
        index = random.randrange(len(list_of_containers))  # random value from 0 to length (of the list of containers)
        container_to_stop = list_of_containers[index]
        # stop the chosen container
        logging.info("%s - Container stopped: %s\n", datetime.now(), container_to_stop.name)
        container_to_stop.stop()


if __name__ == '__main__':
    logging.basicConfig(filename='execution.log', level=logging.INFO)
    logging.info("%s - Antagonist started\n"
                 "Interval between periodic attacks: %d\n", datetime.now(), INTERVAL_BETWEEN_ATTACKS)

    # Instantiate the Docker client
    client = docker.from_env()
    while 1:
        periodic_attack()
        time.sleep(INTERVAL_BETWEEN_ATTACKS)
