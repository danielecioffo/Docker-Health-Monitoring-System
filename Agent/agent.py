import logging
import docker
import time
from datetime import datetime
import subprocess
from subprocess import PIPE

INTERVAL_BETWEEN_PINGS = 10  # Seconds between periodic checks
THRESHOLD = 50  # Packet loss threshold
MONITORED_LIST = [
    "dummy_one",
    "dummy_two",
    "dummy_three"
]


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


def periodic_check():
    """
    Function to be called periodically to monitor the state of all containers in MONITORED_LIST
    """
    for monitored in MONITORED_LIST:
        container = client.containers.get(monitored)
        # Since local attributes are cached, we must call reload() to refresh attrs
        container.reload()
        ip_address = container.attrs['NetworkSettings']['IPAddress']
        # If the container is not running it is not connected to the network
        if ip_address == "":
            logging.warning("Container %s is down. Restarting it...", monitored)
            container.restart()
        else:
            loss = ping(ip_address)
            if loss >= THRESHOLD:
                logging.warning("Container %s is experiencing %f%% packet loss. Restarting it...", monitored, loss)
                container.restart()
            else:
                logging.info("Container %s is working correctly", monitored)


if __name__ == '__main__':
    logging.basicConfig(filename='execution.log', level=logging.INFO)
    logging.info("%s - Agent started\n"
                 "Interval between periodic checks: %d\n"
                 "Packet loss threshold: %d", datetime.now(), INTERVAL_BETWEEN_PINGS, THRESHOLD)

    # Instantiate a Docker client
    client = docker.from_env()
    while 1:
        logging.info("%s - Checking the state of containers...", datetime.now())
        periodic_check()
        time.sleep(INTERVAL_BETWEEN_PINGS)
