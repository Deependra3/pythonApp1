# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy everything from the New folder directory into the container at /app
COPY ./New\ folder /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Verify if the file is copied into the Docker image
RUN ls -l /app

# CMD to run app.py when the container launches
CMD ["python", "app.py"]