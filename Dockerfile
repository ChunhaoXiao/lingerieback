
FROM python:3.12


WORKDIR /code

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY ./requirements.txt /code/requirements.txt

COPY ./data/init.sql /code/init.sql

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "8017"]