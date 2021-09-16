FROM python:3.8.12-slim-buster
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN flask db upgrade
# дадим немного контента и лишних табличек в базе
RUN python models.py

CMD python3 app.py