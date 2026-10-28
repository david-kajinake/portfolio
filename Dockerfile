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
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py shell -c 'import os; from django.contrib.auth import get_user_model; User = get_user_model(); username = os.environ.get(\"DJANGO_SUPERUSER_USERNAME\"); email = os.environ.get(\"DJANGO_SUPERUSER_EMAIL\", \"\"); password = os.environ.get(\"DJANGO_SUPERUSER_PASSWORD\"); exists = User.objects.filter(username=username).exists() if username else False; User.objects.create_superuser(username=username, email=email, password=password) if username and password and not exists else None; print(\"Superuser created.\" if username and password and not exists else \"Superuser creation skipped (credentials missing or username already exists).\")' && python -m gunicorn personal_portfolio.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]





