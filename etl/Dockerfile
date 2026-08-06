FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir psycopg2-binary

WORKDIR /app

COPY populate_dwh.py run_etl.py ./

CMD ["python", "run_etl.py"]
