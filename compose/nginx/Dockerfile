FROM nginx:1.25-alpine

# Remover a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar a configuração personalizada
COPY nginx.conf /etc/nginx/conf.d/
