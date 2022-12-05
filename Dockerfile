# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# check current dir status
RUN pwd
RUN ls

# Install dependencies
RUN pip install -r requirements.txt

# 執行python的指令語法
CMD ["python","app.py"]