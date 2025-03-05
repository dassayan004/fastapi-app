# Use an official Python image
FROM python:3.12.0-alpine

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev python3-dev libffi-dev

# Copy the rest of the application files
COPY . .

# Expose port
EXPOSE 8000

# Set the command to execute the batch file
CMD ["fastapi", "run", "src/main.py"]
