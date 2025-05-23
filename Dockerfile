# 1. Build stage: install dependencies
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Runtime stage
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages \
                     /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Optional: if you want Flask's debug/auto-reload in other envs
ENV FLASK_ENV=production

# Expose the port your script listens on
EXPOSE 5000

# Run your app by invoking Python directly
CMD ["python", "run.py"]
