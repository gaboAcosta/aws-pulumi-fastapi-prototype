FROM python:3.10-alpine3.20

RUN \
 apk add build-base linux-headers && \
 apk add --no-cache postgresql-libs libffi-dev && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

WORKDIR /application

COPY ./ /application/
RUN pip install --no-cache-dir --upgrade -r /application/requirements.txt

EXPOSE 80

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
