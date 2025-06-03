# worker/Dockerfile
FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && update-ca-certificates

COPY requirements.txt ./

RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

CMD ["python", "watcher.py"]
