FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN apk add tzdata

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]