FROM python:3.13-slim-bookworm

WORKDIR /script

# Copy only the requirements.txt first to take advantage of Docker caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create output directory
RUN mkdir -p output

CMD ["python", "script.py"]