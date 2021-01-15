FROM python:3.9.1-slim 

WORKDIR /app 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt 

RUN mkdir uploads && mkdir private

COPY . .

# create db tables
RUN python -c "from main import db; db.drop_all(); db.create_all()"

# start server with 4 workers 

CMD ["gunicorn","-w", "4", "main:app", "-b", "0.0.0.0:8080"]

