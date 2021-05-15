# Dummy Container
This directory contains the code to be run in those containers whose health must be monitored.

They will be _dummy containers_; the code will simply keep them running by periodically printing a message. 

In order to build the image, run the following command:
`docker build -t dummy .`

In order to run the container in background, run the following command:
`docker run -d --name dummy_# dummy` where `#` is the number of the container (for example, `one`)