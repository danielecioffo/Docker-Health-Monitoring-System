import logging
import threading
import docker
import time
import socket
from datetime import datetime
import subprocess
from subprocess import PIPE
import communication
import config

# Instantiate a Docker client
client = docker.from_env()
# Lock to be acquired in order to read/write into shared variables
lock = threading.Lock()


def add_to_monitored(container_name):
    """
    :param container_name: name of the container to be added to the list of monitored containers
    """
    # Check if there is a container with that name on the host
    container_list = client.containers.list(all=True)
    name_list = []
    for container in container_list:
        name_list.append(container.name)
    if container_name not in name_list:
        logging.warning("There is no container named %s on this host, "
                        "so it cannot be added to the list to be monitored", container_name)
        return
    with lock:
        # Avoid duplicate entries in the list
        if container_name in config.MONITORED_LIST:
            logging.warning("Container %s in already in the list to be monitored, "
                            "so it cannot be added to it", container_name)
            return
        config.MONITORED_LIST.append(container_name)


def remove_from_monitored(container_name):
    """
    :param container_name: name of the container to be removed from the list of monitored containers
    """
    with lock:
        try:
            config.MONITORED_LIST.remove(container_name)
        except:
            logging.warning("Container %s is not in the list of monitored ones, "
                            "therefore it cannot be removed", container_name)


def change_threshold(new_value):
    """
    :param new_value: new threshold
    """
    with lock:
        config.THRESHOLD = new_value


def report_container_status():
    """
    :return: a list containing all containers present on the machine and their status
    """
    container_list = client.containers.list(all=True)
    status_list = []
    for container in container_list:
        status = container.status
        name = container.name
        hostname = socket.gethostname()
        if container.name in config.MONITORED_LIST:
            monitored = True
        else:
            monitored = False
        status_list.append({'hostname': hostname, 'name': name, 'status': status, 'monitored': monitored})

    return status_list


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
    Function to be called periodically to monitor the state of containers
    :param to_be_monitored: list of containers to be monitored
    :param threshold: threshold for packet loss
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
            # Ping the container and calculate the packet loss
            loss = ping(ip_address)
            # If the packet loss is lower than the threshold nothing has to be done
            if loss < threshold:
                logging.info("Container %s is experiencing %.2f%% packet loss (under the selected threshold for "
                             "restart)", monitored, loss)
            # If the packet loss is higher than the threshold the container must be restarted
            else:
                logging.warning("Container %s is experiencing %.2f%% packet loss. Restarting it...", monitored, loss)
                container.restart()


def agent_thread():
    """
    Function to be run by the agent thread that must check the status of the system
    """
    logging.info("%s - Agent started", datetime.now())
    logging.info("Interval between periodic checks: %d", config.INTERVAL_BETWEEN_PINGS)
    while 1:
        with lock:
            local_threshold = config.THRESHOLD
            local_list = config.MONITORED_LIST.copy()
        logging.info("Packet loss threshold: %.2f", local_threshold)
        logging.info("List of containers to be monitored: [%s]" % ', '.join(local_list))
        logging.info("%s - Checking the state of containers...", datetime.now())
        periodic_check(local_list, local_threshold)
        time.sleep(config.INTERVAL_BETWEEN_PINGS)


if __name__ == '__main__':
    logging.basicConfig(filename='execution.log', level=logging.INFO)

    # Start agent thread
    agent = threading.Thread(target=agent_thread)
    agent.start()

    # Initialize the communication
    communication.initialize_communication()
