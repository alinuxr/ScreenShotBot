FROM python:latest
COPY ./ /
RUN apt-get update && apt-get install -y python3-pip
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]