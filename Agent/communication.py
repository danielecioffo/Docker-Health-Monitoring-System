# consume messages from REST interface
import pika


def change_treshold(val):
    print('Hello')
    # change threshold


def activate_deactivate_container(container_name, hostname, new_status):
    print('Hello')
    # change the status of the selected container


def provide_list_of_containers():
    """
    callback when the status is asked
    collects the status from each container and publishes it into the relative topic
    """
    string = ''  # find status of containers

    channel.queue_declare(queue='list_response')
    channel.basic_publish(exchange='', routing_key='list_response', body=string)
    connection.close()


def generic_callback(ch, method, properties, body):
    print("Hello, message received")
    # parse message, call the correct method
    # if topic is threshold, call change threshold
    # if topic is list_request, call provide_list_of_containers
    # if topic is actives, call activate_deactivate_container


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
