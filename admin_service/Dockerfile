FROM python:latest

WORKDIR /app

COPY . .

RUN apt-get -y update
RUN apt-get -y upgrade
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "./src/main.py"]
