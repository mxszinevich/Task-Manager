FROM nginx:1.21-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY start.sh .
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
