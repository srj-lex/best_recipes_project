FROM python:3.9

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["/bin/bash", "run.sh"]
