FROM python:3.11
WORKDIR /code/app
EXPOSE 9980

# python setup
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# push app
RUN pip install fastapi uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9980","--reload"]