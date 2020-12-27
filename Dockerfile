FROM python:3.9-buster

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libpq-dev

COPY /requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP /app/labs_wishlist.py 

COPY . /app

ENTRYPOINT ["flask"]

CMD ["run", "--host", "0.0.0.0"]