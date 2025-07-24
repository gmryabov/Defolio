FROM python:3.12

WORKDIR /app/backend

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "Defolio", "worker", "--loglevel=info"]
