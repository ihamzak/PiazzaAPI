FROM python:3.7.3-stretch

ENV  PYTHONBUFFERED 1
## Step 1:
# Create a working directory
WORKDIR /app/

## Step 2:
# Copy source code to working directory
COPY . /app/

## Step 3:
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

## Step 4:
# Expose port 80
EXPOSE 80

## Step 5:
# Run app.py at container launch
CMD python manage.py runserver 0.0.0.0:8000
