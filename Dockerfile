FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src .

COPY ./entrypoint.sh ./
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]

EXPOSE 80
