FROM python:3.10-alpine

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "run:app","run", "--host=0.0.0.0", "--reload"]