FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
COPY .env /app

RUN pip install --upgrade pip && pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./core /app/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]