import connexion
import six

from swagger_server import util


def put_threshold(thresholdValue):  # noqa: E501
    """Update packet loss threshold

    Update packet loss threshold used in netem in the hosts&#39; containers # noqa: E501

    :param thresholdValue: New value threshold
    :type thresholdValue: int

    :rtype: None
    """
    return 'do some magic!'
