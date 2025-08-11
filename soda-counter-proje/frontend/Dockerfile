# Resmi Nginx imajını kullan
FROM nginx:1.25-alpine

# `index.html` dosyasını Nginx'in sunacağı dizine kopyala
COPY index.html /usr/share/nginx/html/index.html

# Nginx'i reverse proxy olarak yapılandıracak dosyayı kopyala
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 8080 portunu aç
EXPOSE 8080
