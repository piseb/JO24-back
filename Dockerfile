FROM python:3.12-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src .
ENTRYPOINT [ "python" ]
CMD [ "manage.py", "runserver", "0.0.0.0:8000" ]
EXPOSE 8000
