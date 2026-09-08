# Koyarwa — Frontend

SPA **React + [Fluent UI v9](https://react.fluentui.dev/)**, bâtie avec **Vite**.

- Composants : `@fluentui/react-components`
- Icônes : `@fluentui/react-icons` (Fluent icon pack)
- Police : **Google Sans** (avec repli Roboto — voir plus bas)

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
│   ├── fonts.css           # @font-face Google Sans (optionnel, voir ci-dessous)
│   └── global.css          # reset + police de base
├── api/
│   └── client.js           # client HTTP vers l'API backend
├── components/
│   └── HealthCard.jsx       # exemple : appelle GET /api/v1/health
└── assets/fonts/            # emplacement des .woff2 Google Sans (voir son README)
```

## Configuration

`VITE_API_BASE_URL` (dans `.env`) pointe vers l'API backend
(défaut : `http://localhost:8000`).

## Thème & police

Le thème Fluent est personnalisé dans `theme/koyarwaTheme.js` : on repart des
thèmes officiels (`webLightTheme` / `webDarkTheme`) et on surcharge la police de
base (`fontFamilyBase`), qui se propage à tous les composants Fluent.

**Google Sans** est propriétaire et non distribuable : elle n'est donc pas
embarquée. L'app utilise **Roboto** (chargée depuis Google Fonts) comme repli
fidèle. Pour activer Google Sans, voir [`src/assets/fonts/README.md`](src/assets/fonts/README.md).
