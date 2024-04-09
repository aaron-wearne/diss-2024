FROM python:3.11 

COPY . .

ENV PYTHONUNBUFFERED=1

#WORKDIR /code/Project

#COPY . /code/ 

#COPY requirements.txt .

RUN pip install -r requirements.txt 

EXPOSE 8000

ENTRYPOINT [ "python", "Project/manage.py", "runserver" ]