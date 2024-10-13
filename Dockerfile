# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder into the container
COPY . .

# Expose the port that your app runs on
EXPOSE 8000

# Command to run the application
CMD [ "uvicorn", "clusterblog:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
