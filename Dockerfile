FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

COPY server.py .

EXPOSE 8080

CMD ["python", "server.py"]