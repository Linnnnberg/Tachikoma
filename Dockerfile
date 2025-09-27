# Tachikoma Multi-Agent AI System - Production Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p exports logs agent_states conversation_cache role_templates model_cache performance_logs

# Set environment variables
ENV PYTHONPATH=/app
ENV TACHIKOMA_LOG_LEVEL=INFO
ENV TACHIKOMA_ENABLE_CACHING=true

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["python", "-m", "tachikoma.main"]
