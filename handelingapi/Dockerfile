FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y\
    gcc\
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p logs

RUN pip install -r requirements.txt

EXPOSE 8002

CMD ["uvicorn" , "handelingapi:handelapp", "--host", "0.0.0.0" , "--port" , "8002" ]