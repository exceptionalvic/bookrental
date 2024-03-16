FROM nginx:1.19.8

RUN rm /etc/nginx/conf.d/default.conf


COPY nginx.conf /etc/nginx/nginx.conf

COPY bookrental.conf /etc/nginx/conf.d/bookrental.conf