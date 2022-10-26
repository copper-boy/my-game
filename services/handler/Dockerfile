FROM python:3.10

WORKDIR /app

COPY . .

RUN python -m pip install -q --upgrade pip -r requirements.txt

CMD echo "[+] Run handler" && \
    while !nc -z handler_db 5432; do sleep 1; done && \
    python app/main.py
