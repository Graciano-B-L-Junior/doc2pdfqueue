FROM python:3.10-bookworm

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "flask","--app","service","run","--debug", "--host=0.0.0.0"  ]