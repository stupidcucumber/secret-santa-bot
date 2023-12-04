FROM python

RUN apt-get update

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache -r requirements.txt

COPY . ./

ENTRYPOINT [ "python3" ]
CMD [ "main.py", "--config-path", "config.yaml", "--database", "data_test.db", "-c" ]