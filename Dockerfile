# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the script to generate config.json from environment variables
RUN python generate_config.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Run Flask when the container launches
CMD ["python", "app.py"]
