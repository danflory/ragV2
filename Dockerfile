# 1. Use the same lightweight base
FROM python:3.12-slim

# 2. Optimization: Prevent python from buffering stdout (logs appear faster)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Set work directory
WORKDIR /app

# 4. System dependencies (kept your git addition)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python deps (Cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code
# Using '.' matches the WORKDIR.
COPY . .

# 7. Expose Port
EXPOSE 5050

# 8. Start command
# We explicitly call the module from the current directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050", "--reload"]