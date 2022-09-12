FROM python:3

RUN mkdir -p /opt/src/shop/buyer
WORKDIR /opt/src/shop/buyer

COPY shop/models.py ./models.py
COPY shop/configuration.py ./configuration.py
COPY shop/requirements.txt ./requirements.txt
COPY shop/buyer/application.py ./application.py
COPY shop/buyer/buyerDecorator.py ./buyerDecorator.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shop/buyer"

ENTRYPOINT ["python", "./application.py"]
