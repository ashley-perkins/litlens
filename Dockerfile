# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /code

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Hugging Face expects (match your space.yaml)
EXPOSE 7860

# Command to run the app
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]

RUN pip install --upgrade pip
