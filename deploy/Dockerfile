FROM python:3.9-slim


WORKDIR /app


COPY . /app


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirement.txt


EXPOSE 5000



CMD ["python", "app.py"]
