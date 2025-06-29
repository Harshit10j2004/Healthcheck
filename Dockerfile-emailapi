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

EXPOSE 8000

CMD ["uvicorn" , "emailapi:emailapp", "--host", "0.0.0.0" , "--port" , "8000" ]