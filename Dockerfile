# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip3 install --trusted-host pypi.python.org

# Make port 62000 available to the world outside this container
EXPOSE 62000

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run the python command to start the server
CMD ["python", "server.py"]
