
FROM python:3.12.6

WORKDIR /personal-assistant

COPY . .


RUN pip install pipenv


RUN pipenv install --system --deploy

CMD ["python", "task.py"]