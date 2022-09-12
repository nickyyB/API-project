FROM python:3

RUN mkdir -p /opt/src/shop/admin
WORKDIR /opt/src/shop/admin

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/requirements.txt ./requirements.txt
COPY shop/admin/application.py ./application.py
COPY shop/admin/adminDecorator.py ./adminDecorator.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop/admin"

ENTRYPOINT ["python", "./application.py"]
