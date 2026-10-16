FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY cells/ ./cells/
COPY cortex/ ./cortex/
COPY synapses/ ./synapses/
COPY engine.py .
COPY SOUL.md .

CMD ["python", "engine.py"]
