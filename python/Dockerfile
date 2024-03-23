# Slim solventa error de pandas
FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

# Solventa error de psycopg2
RUN apt-get update \
	&& apt-get install -y libpq-dev gcc \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "run:app","run", "--host=0.0.0.0", "--reload"]