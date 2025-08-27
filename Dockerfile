FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project (so NEW/app.py becomes /app/NEW/app.py)
COPY . /app
RUN mkdir -p /app/data

EXPOSE 8501

# IMPORTANT: point Streamlit to NEW/app.py
CMD ["python", "-m", "streamlit", "run", "NEW/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
