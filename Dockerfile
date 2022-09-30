FROM python:3.9-buster

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 app.py