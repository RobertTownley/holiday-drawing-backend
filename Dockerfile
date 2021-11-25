FROM python:3

ENV PYTHONUNBUFFERED=1

RUN mkdir /backend
expose 8000
WORKDIR /backend

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD /backend/entrypoint.sh
