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
    activate_deactivate_posting(hostname, containerName, 'False')
    return 'Successful operation!'


def get_containers():  # noqa: E501
    """Retrieve all containers

    Retrieve the list of all containers with their informations # noqa: E501


    :rtype: List[Container]
    """
    return_value = []

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.3.172'))
    channel = connection.channel()
    # ASK FOR CONTAINERS
    channel.exchange_declare(exchange='topics', exchange_type='topic')
    channel.basic_publish(exchange='topics', routing_key='list_request', body='')

    # FETCH INFORMATIONS FROM CONTAINERS
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='topics', queue=queue_name, routing_key='list_response')
    i = 0
    while i != 1:
        method_frame, header_frame, body = channel.basic_get(queue=queue_name)
        if method_frame is not None:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            body_array = json.load(body)
            for value in body_array:
                return_value.append(
                    Container(name=value.get('name'), host=value.get('hostname'), monitor=value.get('monitored'),
                              status=value.get('status')))
            i += 1

    connection.close()

    return return_value


def post_container(hostname, containerName):  # noqa: E501
    """Monitor specified container

    Monitor container specified in the path # noqa: E501

    :param hostname: Name of the host
    :type hostname: str
    :param containerName: Name of a container inside a host
    :type containerName: str

    :rtype: None
    """
    activate_deactivate_posting(hostname, containerName, 'True')
    return 'Successful operation!'


def activate_deactivate_posting(hostname, container_name, new_status):
    """

    Publish in a specific queue the message either to remove or add to the
    monitored a specific container hosted on a particular host

    :param hostname: name of the host
    :type hostname: str
    :param container_name: name of a container inside a host
    :type container_name: str
    :param new_status: indicate if it is a delete or a post ('False' or 'True')
    :type new_status: str
    :return:
    """
    body_tuple = (hostname, container_name, new_status)
    body_string = str(body_tuple)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.3.172'))
    channel = connection.channel()
    channel.exchange_declare(exchange='topics', exchange_type='topic')
    channel.basic_publish(exchange='topics', routing_key='actives', body=body_string)
    connection.close()
