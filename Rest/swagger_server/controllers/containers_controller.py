import connexion
import six
import pika
import json

from swagger_server.models.container import Container  # noqa: E501
from swagger_server import util


def delete_monitored_container(hostname, containerName):  # noqa: E501
    """Unmonitor specified container

    Unmonitored container specified in the path # noqa: E501

    :param hostname: Name of the host
    :type hostname: str
    :param containerName: Name of a container inside a host
    :type containerName: str

    :rtype: None
    """
    return 'do some magic!'


def get_containers():  # noqa: E501
    """Retrieve all containers

    Retrieve the list of all containers with their informations # noqa: E501


    :rtype: List[Container]
    """
    returnValue = []
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.3.172'))
    channel = connection.channel()
    channel.queue_declare(queue='list_response')
    method_frame, header_frame, body = channel.basic_get(queue='list_response')
    if method_frame.NAME is None:
        pass # TODO: rifare la richiesta se questo caso è possibile
    else:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        bodyArray = json.load(body)
        for value in bodyArray:
            returnValue.append(Container(name=value.get('name'), host=value.get('hostname'), monitor=value.get('monitored'), status=value.get('status')))

    return returnValue


def post_container(hostname, containerName):  # noqa: E501
    """Monitor specified container

    Monitor container specified in the path # noqa: E501

    :param hostname: Name of the host
    :type hostname: str
    :param containerName: Name of a container inside a host
    :type containerName: str

    :rtype: None
    """
    return 'do some magic!'
