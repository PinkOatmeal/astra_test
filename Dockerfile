FROM python:3.9.6-slim

WORKDIR usr/src/ip2location

COPY . ./

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "start.py"]