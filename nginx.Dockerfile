FROM nginx:stable-alpine

# Copier la configuration nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Préparer le répertoire pour les fichiers statiques
RUN rm -rf /usr/share/nginx/html/*

# Copier les fichiers du build frontend (le dossier 'out' de l'export statique Next.js)
COPY frontend/out/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 