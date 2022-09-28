FROM python:latest

WORKDIR /app

# copy the dependencies file to the working directory

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requierments.txt .
#COPY ./requierments.txt /app/requierments.txt

RUN pip install -r requierments.txt

COPY main.py ./
RUN mkdir ./templates 
RUN mkdir ./stdout
COPY templates/index.html ./templates/
COPY templates/files.html ./templates/
EXPOSE 5000

CMD [ "python", "./main.py"]
