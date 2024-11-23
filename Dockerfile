# Use an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY count_files_and_upload.py /app/

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "count_files_and_upload.py"]
