FROM python:3.7-slim
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/bin/bash"]
CMD ["./startapp.sh"]