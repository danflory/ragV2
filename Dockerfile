# 1. Use an official lightweight Python runtime
FROM python:3.12-slim

# 2. Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Ensures logs are flushed directly to terminal (great for debugging)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install system dependencies (needed for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements first (Layer Caching strategy)
# This means if you change your code but not your requirements, 
# Docker won't have to re-install everything.
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the actual application code
COPY app/ ./app/

# 8. Expose the port the app runs on
EXPOSE 5050

# 9. Define the command to run the app
# We use direct uvicorn execution for simplicity in the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050"]