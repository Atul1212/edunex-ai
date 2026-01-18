FROM python:3.9-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Permissions for script
COPY render_build.sh .
RUN chmod +x render_build.sh

# Expose Port (Render automatically sets $PORT)
EXPOSE 8501

# Start Command
CMD ["./render_build.sh"]

# FROM python:3.10-slim

# # Set working directory
# WORKDIR /app

# # Copy requirements and install
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all code
# COPY . .

# # The command will be overridden by docker-compose
# CMD ["python", "--version"]

