FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN apt-get update && apt-get install libpq-dev gcc  -y
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime \
    && echo "America/Sao_Paulo" > /etc/timezone

RUN apt-get autoremove -y gcc && \
    apt-get clean
RUN rm -rf /var/cache/apt/archives && rm -rf /var/lib/apt/lists/*

COPY . ./
WORKDIR /app

CMD ["flask", "run", "--host", "0.0.0.0"]
