import { webDarkTheme, webLightTheme } from "@fluentui/react-components";

/**
 * Police de base de l'app : « Google Sans », chargée depuis Google Fonts dans
 * index.html. Le token `fontFamilyBase` se propage à tous les composants Fluent.
 */
export const fontFamilyBase =
  "'Google Sans', 'Segoe UI', system-ui, -apple-system, sans-serif";

// On part des thèmes Fluent officiels et on ne surcharge que la police de base :
// le token `fontFamilyBase` se propage à tous les composants Fluent.
export const koyarwaLightTheme = { ...webLightTheme, fontFamilyBase };
export const koyarwaDarkTheme = { ...webDarkTheme, fontFamilyBase };
