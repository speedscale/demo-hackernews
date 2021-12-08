FROM python:3 as hndemo

WORKDIR /usr/src/app

COPY . .

ENV CONTAINER_MODE=1

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./hn.py" ]

EXPOSE 8080