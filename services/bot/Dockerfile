FROM python:latest

WORKDIR /app

COPY . .

RUN python -m pip install poetry
RUN python -m poetry config virtualenvs.create false && \
    python -m poetry install --no-interaction --no-ansi

CMD echo "[+] Run bot" && \
    python app/main.py
