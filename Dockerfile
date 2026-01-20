FROM python:3.13

ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run Flask app with Gunicorn (WSGI)
CMD gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 2 --timeout 60 app:app
