import docker

if __name__ == '__main__':
    client = docker.from_env()
    list_of_containers = client.containers.list()
    for container in list_of_containers:
        print('Container ID: ' + container.id + '\n')
    list_of_images = client.images.list()
    print(list_of_images)
