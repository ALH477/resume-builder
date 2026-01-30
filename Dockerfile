FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/ALH477/resume-builder"
LABEL org.opencontainers.image.description="Web-based resume builder - Flask interface"
LABEL org.opencontainers.image.version="1.1.0"
LABEL maintainer="ALH477"

WORKDIR /app

# Install Python dependencies
COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

# Copy application files
COPY web_app.py .
COPY html_generator.py .
COPY templates/ templates/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/', timeout=5)"

CMD ["python", "web_app.py", "--host", "0.0.0.0", "--port", "5000"]
