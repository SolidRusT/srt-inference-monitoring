# Deployment Guide

This document outlines the steps required to deploy the Performance Monitor application in a production environment.

## Prerequisites

1. **Docker**: Ensure Docker is installed on the host machine.
2. **Docker Compose**: Ensure Docker Compose is installed.
3. **Configuration**: Update the `config.yaml` file with production server details.

## Steps

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/SolidRusT/srt-inference-monitoring.git
cd srt-inference-monitoring
```

### 2. Update Configuration

Ensure your `config.yaml` file is correctly configured with your production server details. If you have different configurations for development and production, create a separate `config-prod.yaml` and update the Docker Compose file to use it.

### 3. Build and Run with Docker Compose

Build and run the application using Docker Compose:

```bash
docker-compose up -d --build
```

This command will build the Docker images and start the containers in detached mode.

### 4. Verify Deployment

Once the containers are up and running, verify the deployment by accessing the dashboard:

```url
http://<your-server-ip>:5000
```

### 5. Scaling

To scale the application horizontally, update the `docker-compose.yml` file to specify the number of replicas:

```yaml
services:
  app:
    ...
    deploy:
      replicas: 3
    ...
```

### 6. Stopping the Application

To stop the application, use the following command:

```bash
docker-compose down
```

This command will stop and remove the containers.

### 7. Logs and Monitoring

To view the logs of the running application:

```bash
docker-compose logs -f
```

## Notes

- **Environment Variables**: Ensure the necessary environment variables are set for production.
- **Data Persistence**: Ensure data persistence is properly configured for the Valkey service.

By following these steps, you should be able to deploy the Performance Monitor application in a production environment effectively.
