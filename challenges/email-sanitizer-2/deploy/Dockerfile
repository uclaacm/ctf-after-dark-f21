FROM php:7.0-apache
COPY *.php /var/www/html/
COPY *.txt /var/www/html/
RUN chown -R root:root /var/www/html
RUN chmod -R 775 /var/www/html/

# RUN chmod 700 /