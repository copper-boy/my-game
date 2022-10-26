FROM python:3.10

WORKDIR /app

COPY . .

RUN python -m pip install -q --upgrade pip -r requirements.txt

CMD echo "[+] Run api" && \
    while !nc -z api_db 5432; do sleep 1; done && \
    uvicorn app.main:app --reload --host 0.0.0.0 --port 14961
