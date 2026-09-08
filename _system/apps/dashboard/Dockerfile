FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WIKI_DIR=/wiki \
    ADR_DIR=/adr \
    RAW_SOURCES_DIR=/sources

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates
COPY static ./static

EXPOSE 8000

# One worker keeps the lifecycle state (last-seen timestamp, watchdog) coherent
# in a single process. A few threads handle a page render and the occasional
# lightweight /ping heartbeat concurrently. No request is held open anymore
# (the heartbeat replaced the SSE /events stream), so a small pool suffices and
# can never be starved — /stop is always serviceable. See ADR-0022.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", \
     "--worker-class", "gthread", "--workers", "1", "--threads", "4", \
     "app:app"]
