FROM python:3

RUN mkdir -p /opt/src/shop/deamon
WORKDIR /opt/src/shop/deamon

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/requirements.txt ./requirements.txt
COPY shop/deamon/application.py ./application.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop/deamon"

ENTRYPOINT ["python", "./application.py"]
