#Deriving the latest base image
FROM python:latest


# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /app

# copy the dependencies file to the working directory
#COPY requierments.txt .
COPY ./requierments.txt /app/requierments.txt
# install dependencies
RUN pip install -r requierments.txt
#to COPY the remote file at working directory in container
COPY main.py ./
# Now the structure looks like this '/usr/app/src/test.py'


#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./main.py"]

#docker image build -t python:0.0.1 /home/roushan/Desktop/docker_2/docker_assignment