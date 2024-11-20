
FROM python:3.11


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

COPY ./data/init.sql /code/init.sql


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "8017"]