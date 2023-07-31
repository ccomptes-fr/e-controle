ARG DOCKER_REGISTRY

# Build the front
FROM ${DOCKER_REGISTRY}node/node16:16.14.2-build AS front
ARG REGISTRY_DOMAINE
ARG NEXUS_URL
ARG NEXUS_HOST
WORKDIR /code
COPY package*.json /code/
COPY . .
RUN npm ci --registry=http://${REGISTRY_DOMAINE}/repository/npm/ && npm run build-all

# Build the back
FROM ${DOCKER_REGISTRY}python:3.9.13
ENV PYTHONUNBUFFERED 1
ARG REGISTRY_DOMAINE
ARG NEXUS_URL
ARG NEXUS_HOST

# Update packages
RUN export http_proxy=${PROXY_CC_URL} && apt-get update && apt-get upgrade -y && apt-get install -y locales \
    && sed -i -e 's/# fr_FR.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8/' /etc/locale.gen && locale-gen \
# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8
ENV TZ Europe/Paris
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt --index-url ${NEXUS_URL} --trusted-host ${NEXUS_HOST}
COPY . .
COPY --from=front /code/static/ /code/static
COPY --from=front /code/node_modules/bootstrap/dist/ /code/node_modules/bootstrap/dist
COPY --from=front /code/node_modules/jquery/dist/ /code/node_modules/jquery/dist
RUN chmod a+x ./start.sh

CMD ["./start.sh"]
