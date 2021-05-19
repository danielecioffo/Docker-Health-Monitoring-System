import connexion
import six

from swagger_server.models.container import Container  # noqa: E501
from swagger_server import util


def delete_monitored_container(containerName):  # noqa: E501
    """Unmonitore specified container

    Unmonitored container specified in the path # noqa: E501

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
    return 'do some magic!'


def post_container(containerName):  # noqa: E501
    """Monitore specified container

    Monitore container specified in the path # noqa: E501

    :param containerName: Name of a container inside a host
    :type containerName: str

    :rtype: None
    """
    return 'do some magic!'
