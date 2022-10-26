FROM python:latest

WORKDIR /app

COPY . .

RUN python -m pip install poetry
RUN python -m poetry config virtualenvs.create false && \
    python -m poetry install --no-interaction --no-ansi

CMD echo "[+] Run handler" && \
    while !nc -z handler_db 5432; do sleep 1; done && \
    python app/main.py
