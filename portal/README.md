# Koyarwa — Portal

SPA **React + [Fluent UI v9](https://react.fluentui.dev/)**, bâtie avec **Vite**.

- Composants : `@fluentui/react-components`
- Icônes : `@fluentui/react-icons` (Fluent icon pack)
- Police : **Google Sans** (Google Fonts)

## Prérequis
- Node.js 20+
- Le backend lancé (voir [`../backend/README.md`](../backend/README.md))

## Installation

```bash
cp .env.example .env      # ajuster VITE_API_BASE_URL si besoin
npm install
npm run dev
```

App sur http://localhost:5173

## Scripts

```bash
npm run dev       # serveur de dev (HMR)
npm run build     # build de production → dist/
npm run preview   # sert le build de production
```

## Arborescence

```
src/
├── main.jsx               # point d'entrée React
├── App.jsx                # FluentProvider + mise en page + bascule de thème
├── theme/
│   └── koyarwaTheme.js     # thèmes Fluent (clair/sombre) + police Google Sans
├── styles/
│   └── global.css          # reset + police de base
├── api/
│   └── client.js           # client HTTP vers l'API backend
└── components/
    └── HealthCard.jsx       # exemple : appelle GET /api/v1/health
```

## Configuration

`VITE_API_BASE_URL` (dans `.env`) pointe vers l'API backend
(défaut : `http://localhost:8000`).

## Thème & police

Le thème Fluent est personnalisé dans `theme/koyarwaTheme.js` : on repart des
thèmes officiels (`webLightTheme` / `webDarkTheme`) et on surcharge la police de
base (`fontFamilyBase`), qui se propage à tous les composants Fluent.

La police par défaut est **Google Sans**, chargée depuis **Google Fonts** dans
`index.html`. Pour l'auto-héberger (perf / hors-ligne), déposer les `.woff2` dans
`src/assets/` et déclarer un `@font-face`.

## Docker

Image de production multi-stage (build Vite → **nginx**) : `Dockerfile` + `nginx.conf`
(fallback SPA + proxy `/api` vers le backend).

```bash
docker build -t koyarwa-portal .
docker run --rm -p 3000:80 koyarwa-portal
```

L'URL de l'API est injectée au build via l'argument `VITE_API_BASE_URL` (défaut
vide = chemins relatifs proxifiés par nginx). Le plus simple reste
`docker compose up --build` à la racine.
