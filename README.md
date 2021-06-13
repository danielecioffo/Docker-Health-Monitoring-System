# Docker-Health-Monitoring-System
Health monitoring system for a set of Docker hosts. The system must monitor the wellbeing of the containers running on the hosts by sending periodic probes. All the details can be found [here](documentation/latex/healthMonitoring.pdf).

## Repository Organization
The project repository is organized as follows:
* *Agent*: module that contains the implementation of the Agent, that acts like a monitor for a specific node (there will be one Agent for each node).
* *Antagonist*: module that contains the implementation of the Antagonist, used to test the system.
* *Broker*: directory that contains a file for the deployment of the RabbitMQ broker.
* *documentation*: directory that contains the LateX source for the report.
* *Dummy Container*: module that contains the implementation of a dummy container, to have something to monitor. It also contains a module to simulate network problems, in order to fully show the Agent's functionalities.
* *Rest*: module that contains the implementation of the server that exposes the REST API, used to access the application functionalities.

## How to run the application
First of all it is important to say that this project was developed for the Cloud Computing university course. Therefore the following information is valid only for the deployment on the virtual machines that were given to us during the course. To use this application in another context it is necessary to modify the modules that make up the system in order to change IP addresses and constants.

To test the application in a simple way, .sh files have been created, to allow faster installation. Thanks to these files it is possible to create a structure to test the functioning of the application in a real context.
Agents uses a broker to exchange indirect and asynchronous messages, so first you need to deploy a container with RabbitMQ. In the Broker folder the [startBroker.sh](Broker/startBroker.sh) file has been created which takes care of this.

Instead, the [start.sh](start.sh) file in the home of the repository starts three dummy containers (useful for having something to monitor), the antagonist (not essential, but allows you to notice the efficiency of the program) and the agent. To remove everything just run the [stop.sh](stop.sh) file.

Finally, in order to interact with the system it is necessary to deploy the server that exposes the REST API. In the Rest folder there is a [start.sh](Rest/start.sh) file that takes care of this. Again a [stop.sh](Rest/stop.sh) file has been prepared to remove everything.
