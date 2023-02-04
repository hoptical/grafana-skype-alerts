FROM python:3.8
WORKDIR /skype
COPY . .
RUN ls ./
RUN pwd
RUN pip install --upgrade pip \
    && pip install -r docker/requirements.txt
EXPOSE 8080
RUN chmod +x docker/entrypoint.sh
ENTRYPOINT ["sh", "docker/entrypoint.sh"]
