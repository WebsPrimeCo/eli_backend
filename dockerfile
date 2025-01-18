FROM python:3.10-slim

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


#ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
