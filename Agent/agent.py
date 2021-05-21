import logging
import threading
import docker
import time
from datetime import datetime
import subprocess
from subprocess import PIPE
import communication

lock = threading.Lock()  # Lock to be acquired in order to read/write into shared variables
INTERVAL_BETWEEN_PINGS = 10  # Seconds between periodic checks
THRESHOLD = 50  # Packet loss threshold
MONITORED_LIST = [
    "dummy_one",
    "dummy_two",
    "dummy_three"
]


def add_to_monitored(container_name):
    MONITORED_LIST.append(container_name)


def remove_from_monitored(container_name):
    MONITORED_LIST.remove(container_name)


def change_threshold(new_value):
    global THRESHOLD
    THRESHOLD = new_value


def ping(address):
    """
    :param address: IP address to be pinged
    :return: percentage of packet loss
    """
    process = subprocess.Popen(['ping', '-c', '5', address], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    packet_loss = float(
        [x for x in stdout.decode('utf-8').split('\n') if x.find('packet loss') != -1][0].split('%')[0].split(' ')[-1])
    return packet_loss


def periodic_check(to_be_monitored, threshold):
    """
    Function to be called periodically to monitor the state of all containers in MONITORED_LIST
    """
    for monitored in to_be_monitored:
        # Try to find the container to be monitored in the list
        try:
            container = client.containers.get(monitored)
        except:
            logging.warning("Container %s is not present on this Docker host.", monitored)
            continue
        # Since local attributes are cached, we must call reload() to refresh attrs
        container.reload()
        ip_address = container.attrs['NetworkSettings']['IPAddress']
        # If the container is not running it is not connected to the network
        if ip_address == "":
            logging.warning("Container %s is down. Restarting it...", monitored)
            container.restart()
        else:
            loss = ping(ip_address)
            if loss >= threshold:
                logging.warning("Container %s is experiencing %f%% packet loss. Restarting it...", monitored, loss)
                container.restart()
            else:
                logging.info("Container %s is experiencing %f%% packet loss (under the selected threshold for restart)",
                             monitored, loss)


def agent_thread():
    """
    Function to be run by the agent thread that must check the status of the system
    """
    logging.info("%s - Agent started", datetime.now())
    logging.info("Interval between periodic checks: %d", INTERVAL_BETWEEN_PINGS)
    while 1:
        with lock:
            local_threshold = THRESHOLD
            local_list = MONITORED_LIST
        logging.info("Packet loss threshold: %d", local_threshold)
        logging.info("%s - Checking the state of containers...", datetime.now())
        periodic_check(local_list, local_threshold)
        time.sleep(INTERVAL_BETWEEN_PINGS)


if __name__ == '__main__':
    logging.basicConfig(filename='execution.log', level=logging.INFO)

    # Instantiate a Docker client
    client = docker.from_env()

    # Start agent thread
    agent = threading.Thread(target=agent_thread)
    agent.start()

    # Initialize the communication
    communication.initialize_communication()
