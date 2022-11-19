FROM openjdk:slim AS base
COPY --from=python:3.9.9-slim / /

WORKDIR /tmp

RUN apt-get clean && apt-get update -y && apt-get install -y git
RUN pip install GitPython==3.1.27

WORKDIR /src

COPY ./*.py /src/
COPY ./*.jar /src/
RUN rm -rf /tmp/

CMD ["main.py"]
ENTRYPOINT ["python"]
