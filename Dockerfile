FROM python:3.8
COPY . /flasky
WORKDIR /flasky
RUN ["pip3", "install", "-r", "requirements.txt"]
EXPOSE 5000
ENV FLASK_APP flasky.py
CMD ["flask", "run", "-h", "0.0.0.0:5000"]
