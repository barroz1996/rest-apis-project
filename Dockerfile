FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["gunicorn","--bind","0.0.0.0.:80", "app:create_app()"]