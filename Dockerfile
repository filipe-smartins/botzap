FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN apt update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run Flask app with Gunicorn (WSGI)
CMD gunicorn --bind 0.0.0.0:8000 --workers 2 app:app
