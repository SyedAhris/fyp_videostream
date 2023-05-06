FROM python:3.10.10

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# RUN apt-get update

# RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8002"]
