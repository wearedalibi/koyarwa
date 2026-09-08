# syntax=docker/dockerfile:1

# ---- build : compile la SPA avec Vite ----
FROM node:22-alpine AS build
WORKDIR /app

# Couche de cache : dépendances seules (installées avant de copier les sources)
COPY package.json package-lock.json ./
RUN npm ci

# Sources + build de production
COPY . .
# URL de l'API injectée au build. Vide = chemins relatifs (l'API est proxifiée
# par nginx via /api). Surchargeable : --build-arg VITE_API_BASE_URL=https://api.exemple.com
ARG VITE_API_BASE_URL=""
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# ---- runtime : nginx sert les fichiers statiques ----
FROM nginx:1.27-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
