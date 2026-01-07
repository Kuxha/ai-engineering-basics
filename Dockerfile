# 1. Base Image: Official Python 3.12 Slim (Small & Fast)
FROM python:3.12-slim

# 2. System Dependencies (Required for some Pydantic/gRPC libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Work Directory
WORKDIR /app

# 4. Install Python Dependencies
# We copy requirements first to leverage Docker Layer Caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the Application Code
COPY . .

# 6. Environment Setup
# We do NOT copy .env. Secrets are injected at runtime for security.
ENV PYTHONUNBUFFERED=1

# 7. Default Command
# We run the Dynamic Router by default
CMD ["python", "phase_6_intelligence/routing/routing_agent.py"]