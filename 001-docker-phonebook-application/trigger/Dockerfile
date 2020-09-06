FROM python:alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python db_init.py