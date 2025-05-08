# Base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Set the Python path to the /app directory
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Prefect requires this to run flows
CMD ["python", "etl/flow.py"]