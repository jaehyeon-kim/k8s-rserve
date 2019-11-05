FROM python:3.7

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

## create a user
RUN useradd pyapi && mkdir /home/pyapi \
    && chown pyapi:pyapi /home/pyapi

USER pyapi
WORKDIR /home/pyapi

## copy source
COPY . /home/pyapi/api

ENTRYPOINT ["uvicorn", "api:app"]
CMD ["--host", "0.0.0.0", "--port", "9000"]