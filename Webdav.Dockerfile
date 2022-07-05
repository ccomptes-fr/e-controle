ARG DOCKER_REGISTRY
FROM ${DOCKER_REGISTRY}python:3.9.13

ENV PYTHONUNBUFFERED 1
ARG PROXY_CC_URL
ARG REGISTRY_DOMAINE
RUN export http_proxy=${PROXY_CC_URL} && echo ${PROXY_CC_URL} && apt-get clean && apt-get update && apt-get install -y locales
RUN sed -i -e 's/# fr_FR.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8
ENV TZ Europe/Paris
WORKDIR /code
RUN mkdir /code/webdav-files /code/e-controle-media
COPY requirements.txt ./
RUN pip install -r requirements.txt --index-url http://${REGISTRY_DOMAINE}/repository/python/simple/ --trusted-host ${REGISTRY_DOMAINE}
RUN pip install WsgiDAV==4.0.1 --index-url http://${REGISTRY_DOMAINE}/repository/python/simple/ --trusted-host ${REGISTRY_DOMAINE}
COPY . .
RUN chmod a+x ./startWebdav.sh

EXPOSE 8081
CMD ["./startWebdav.sh"]
