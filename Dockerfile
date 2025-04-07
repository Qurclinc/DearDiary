FROM python:3.9-slim

WORKDIR /DearDiary

COPY . .

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]