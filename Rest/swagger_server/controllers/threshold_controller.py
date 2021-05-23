import connexion
import six
import pika

from swagger_server import util


def put_threshold(thresholdValue):  # noqa: E501
    """Update packet loss threshold

    Update packet loss threshold used in the Agent # noqa: E501

    :param thresholdValue: New value threshold
    :type thresholdValue: float

    :rtype: None
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.3.172'))
    channel = connection.channel()
    channel.queue_declare(queue='threshold')
    channel.basic_publish(exchange='', routing_key='threshold', body=thresholdValue)
    connection.close()

    return 'Successful operation!'
