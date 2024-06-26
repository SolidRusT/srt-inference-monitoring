# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y curl \
    && pip install --no-cache-dir -r requirements.txt

# Make port 5000 and 8000 available to the world outside this container
EXPOSE 5000
EXPOSE 8000

# Run the application
CMD ["python", "start.py"]
