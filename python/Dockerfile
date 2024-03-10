FROM python:3.10-alpine

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

# Solventa error de psycopg2
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "run:app","run", "--host=0.0.0.0", "--reload"]