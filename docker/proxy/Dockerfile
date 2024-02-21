FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintener="instelce"

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN apk add --no-cache openssl bash && \
    mkdir -p /vol/proxy && \
    chmod 755 /vol/proxy && \
    mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD ["/run.sh"]
