FROM python:3

WORKDIR /src

ADD /src/main.py .

RUN pip install --upgrade pip && \
	pip install click && \
	pip install oyaml

ENTRYPOINT ["python3", "main.py"]
