# Build base image
FROM python:3.13-slim

# Working directory inside the container
WORKDIR /app

# Copy and install dependencies first (so Docker can cache this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

EXPOSE 8080
CMD ["python", "main.py"]