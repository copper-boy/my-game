FROM python:latest

WORKDIR /app

COPY . .

RUN python -m pip install poetry
RUN python -m poetry config virtualenvs.create false && \
    python -m poetry install --no-interaction --no-ansi

CMD echo "[+] Run api" && \
    while !nc -z api_db 5432; do sleep 1; done && \
    uvicorn app.main:app --reload --host 0.0.0.0 --port 14961
