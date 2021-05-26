# consume messages from REST interface
import pika
import socket
import json
import agent


def change_threshold(val):
    print("Received command: change threshold to %d", val)
    agent.change_threshold(val)


def activate_deactivate_container(container_name, hostname, new_status):
    print("Received command: change monitored value of container %s on %d into %s", container_name, hostname, new_status)
    if hostname != socket.gethostname():
        return
    if new_status == 'True':
        agent.add_to_monitored(container_name)
    elif new_status == 'False':
        agent.remove_from_monitored(container_name)
    # change the status of the selected container


def provide_list_of_containers():
    """
    callback when the status is asked
    collects the status from each container and publishes it into the relative topic
    """
    print("Received command: provide list of containers")
    string = json.dumps(agent.report_container_status())  # find status of containers

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.3.172'))  # broker ip address
    channel = connection.channel()
    channel.exchange_declare(exchange='topics', exchange_type='topic')
    channel.basic_publish(exchange='topics', routing_key='list_response', body=string)
    print("I've sent the following answer %s", string)
    connection.close()


def generic_callback(ch, method, properties, body):
    print("Hello, message received")
    # parse message, call the correct method
    # if topic is threshold, call change threshold
    if method.routing_key == 'threshold':
        change_threshold(float(body.decode()))
    # if topic is list_request, call provide_list_of_containers
    elif method.routing_key == 'list_request':
        provide_list_of_containers()
    # if topic is actives, call activate_deactivate_container
    elif method.routing_key == 'actives':
        #body_string = body.decode().replace("(", "").replace(")", "")
        #body_tuple = tuple(map(str, body_string))
        body_tuple = tuple((body.decode.replace("(", "").replace(")", "")).split(','))
        activate_deactivate_container(container_name=body_tuple[1], hostname=body_tuple[0], new_status=body_tuple[2])


def initialize_communication():
    # to embed in a try/exception block

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.3.172'))  # broker ip address
    channel = connection.channel()
    channel.exchange_declare(exchange='topics', exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='topics', queue=queue_name, routing_key='threshold')
    channel.queue_bind(exchange='topics', queue=queue_name, routing_key='list_request')
    channel.queue_bind(exchange='topics', queue=queue_name, routing_key='actives')

    channel.basic_consume(queue=queue_name, on_message_callback=generic_callback, auto_ack=True)
    channel.start_consuming()
