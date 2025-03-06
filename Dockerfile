# Use an official Python runtime as a parent image
FROM python:3.9-slim
LABEL authors="Edward Bird - edwardbirdlab@gmail.com"

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any necessary dependencies
RUN pip install --upgrade pip
RUN pip install .

# Set the default command to run when starting the container
CMD ["ebirdtools"]
