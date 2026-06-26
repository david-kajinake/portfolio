#Pull the base lightweight python version
FROM python:3.13-slim

#set some rules( do not create .pyc files and show server logs immediately )
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Create a /app working directory inside the container
WORKDIR /app

#Install LINUX compilers for some particular libraries like pillow
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

#Copy the requirements list into the container
COPY requirements.txt /app/

#Install the requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copy the actual project code into the container
COPY . /app/

#Tell the container to open port 8000 so that we can access it
EXPOSE 8000


#The command to start the server when the container turns ON
CMD ["python","manage.py","runserver","0.0.0.0:8000"]




