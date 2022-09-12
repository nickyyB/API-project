FROM python:3

RUN mkdir -p /opt/src/shop/supplier
WORKDIR /opt/src/shop/supplier

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/requirements.txt ./requirements.txt
COPY shop/supplier/application.py ./application.py
COPY shop/supplier/supplierDecorator.py ./supplierDecorator.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop/supplier"

ENTRYPOINT ["python", "./application.py"]
