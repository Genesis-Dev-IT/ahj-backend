FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN apt-get update && apt-get install -y dos2unix bash \ 
    && dos2unix /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Run via entrypoint
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Default command to run the Django app with Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "--threads", "4", "--timeout", "120", "genesis.wsgi:application"]