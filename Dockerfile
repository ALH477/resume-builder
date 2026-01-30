FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask

COPY web_app.py /app/
COPY resume_builder.py /app/

EXPOSE 5000

CMD ["python", "web_app.py", "--host", "0.0.0.0", "--port", "5000"]
