# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port on which the app will run
# Make sure this port matches what you configure in your Flask app
EXPOSE 5000

# Run the application using a production-ready server like Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]