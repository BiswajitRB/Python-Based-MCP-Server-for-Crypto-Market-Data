# here we use multi-stage docker file for security purpose and reduce the storage (volume) 
# -------- Stage 1: Builder --------
FROM python:3.11.9-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies (only needed here)  version can be change or avoid->ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential=12.9 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies into a custom folder
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# -------- Stage 2: Runtime --------
FROM python:3.11.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Expose port
EXPOSE 80

# Run FastAPI app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:80"]