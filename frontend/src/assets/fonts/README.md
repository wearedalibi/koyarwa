# Polices

## Google Sans (optionnel)

« Google Sans » est une police **propriétaire** de Google, non distribuée
publiquement : elle n'est donc pas fournie avec ce dépôt.

Si vous disposez d'une licence pour l'utiliser :

1. Déposez ici les fichiers `.woff2`, nommés exactement :
   - `GoogleSans-Regular.woff2`
   - `GoogleSans-Medium.woff2`
   - `GoogleSans-Bold.woff2`
2. Décommentez les blocs `@font-face` dans [`../../styles/fonts.css`](../../styles/fonts.css).

La pile de polices (voir [`../../theme/koyarwaTheme.js`](../../theme/koyarwaTheme.js))
préfère déjà `Google Sans` ; à défaut, l'app utilise **Roboto** (chargée depuis
Google Fonts dans `index.html`), puis les polices système.
