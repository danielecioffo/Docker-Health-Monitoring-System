import connexion
import six
import pika
import json
import logging

from swagger_server import util


def put_threshold(thresholdValue):  # noqa: E501
    """Update packet loss threshold

    Update packet loss threshold used in the Agent # noqa: E501

    :param thresholdValue: New value threshold
    :type thresholdValue: float

    :rtype: None
    """
    if connexion.request.is_json:
        thresholdValue = connexion.request.get_json()
        if type(thresholdValue) is dict:
            thresholdValue = thresholdValue.get('thresholdValue', -1)
        print(str(thresholdValue) + "\n" + str(type(thresholdValue)))

    t_value_float = float(thresholdValue)
    print(t_value_float)

    if not (0 <= t_value_float <= 100):
        return 'Invalid threshold supplied'

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.3.172'))
    channel = connection.channel()
    channel.queue_declare(queue='threshold')
    channel.basic_publish(exchange='', routing_key='threshold', body=t_value_float)
    connection.close()

    return 'Successful operation!'
