FROM python:latest

WORKDIR /app

# copy the dependencies file to the working directory

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requierments.txt .
#COPY ./requierments.txt /app/requierments.txt

RUN pip install -r requierments.txt

COPY main.py ./
COPY server.py ./

CMD [ "python", "./main.py"]

WORKDIR /app/stdout
EXPOSE 80
CMD [ "python", "../server.py"]
