# Use lightweight base image
FROM python:3.11-slim

LABEL maintainer="yourname"
LABEL version="1.0"
LABEL description="FastAPI Dockerized Application"

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl (needed for healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password appuser

# Set working directory
WORKDIR /app

# Copy dependency file first (optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Give permission to user
RUN chown -R appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:5000/health || exit 1

# Run FastAPI app

RUN pip install gunicorn

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]
