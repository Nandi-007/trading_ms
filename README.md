Trading Microservice (trading_ms)

The Trading Microservice is a server application that provides trading functionality via API endpoints. It is built using FastAPI and runs as a standalone microservice.
Prerequisites

    Docker: Ensure that Docker is installed on your system.

Getting Started

Follow the steps below to set up and run the Trading Microservice.

    Clone this repository to your local machine.

    bash

git clone https://github.com/Nandi-007/trading_ms.git

Navigate to the project directory.

bash

cd app

Build the Docker image by running the following command:

    docker build -t trading-platform .

Running the Trading Microservice

To run the Trading Microservice, execute the following command:

css

docker run --network bridge -p 8080:8080 trading-platform

The microservice will start and listen on port 8080. You can access the API endpoints using http://localhost:8080.
API Documentation

The Trading Microservice provides detailed documentation for its API endpoints. After starting the microservice, you can access the API documentation by opening http://localhost:8080/docs in your web browser.
Docker Configuration

The Docker image is built based on the provided Dockerfile. It sets up the necessary dependencies and exposes port 8080 for communication with the microservice.

If you need to customize the Docker configuration, you can modify the Dockerfile according to your specific requirements.
Customization

Feel free to customize the Trading Microservice according to your project requirements. You can modify the API endpoints, add additional functionality, or extend the microservice as needed.