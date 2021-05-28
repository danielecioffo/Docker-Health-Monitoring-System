docker build -t swagger_server .
docker run -d --name swagger_server -p 8080:8080 swagger_server