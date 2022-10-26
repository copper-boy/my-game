FROM python:3.10

WORKDIR /app

COPY . .

RUN python -m pip install -q --upgrade pip -r requirements.txt

CMD echo "[+] Run bot" && \
    python app/main.py
