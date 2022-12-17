FROM nginx:1.21-alpine
RUN apk add --no-cache curl openssl
RUN curl https://get.acme.sh | sh
RUN rm /etc/nginx/conf.d/default.conf
ARG CONF_FILE="nginx.dev.conf"
COPY $CONF_FILE /etc/nginx/conf.d
COPY start.sh .
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
