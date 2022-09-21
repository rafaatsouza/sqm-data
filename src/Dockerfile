FROM openjdk:slim AS base
COPY --from=python:3.9.9-slim / /

WORKDIR /tmp

RUN apt-get clean && apt-get update -y && apt-get install -y git

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r requirements.txt


WORKDIR /src

COPY ./*.py /src/
COPY ./*.jar /src/
RUN rm -rf /tmp/

CMD ["main.py"]
ENTRYPOINT ["python"]
