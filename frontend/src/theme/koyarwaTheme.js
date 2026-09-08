import { webDarkTheme, webLightTheme } from "@fluentui/react-components";

/**
 * Pile de polices de l'app. « Google Sans » (propriétaire) est préférée si elle
 * est disponible ; sinon on retombe sur Roboto (chargée via index.html), puis
 * sur les polices système. Voir src/assets/fonts/README.md pour l'embarquer.
 */
export const fontFamilyBase =
  "'Google Sans', 'Google Sans Text', Roboto, 'Segoe UI', system-ui, -apple-system, sans-serif";

// On part des thèmes Fluent officiels et on ne surcharge que la police de base :
// le token `fontFamilyBase` se propage à tous les composants Fluent.
export const koyarwaLightTheme = { ...webLightTheme, fontFamilyBase };
export const koyarwaDarkTheme = { ...webDarkTheme, fontFamilyBase };
