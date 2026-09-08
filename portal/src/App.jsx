import { useState } from "react";
import {
  Button,
  FluentProvider,
  Subtitle2,
  Title1,
  Tooltip,
  makeStyles,
  tokens,
} from "@fluentui/react-components";
import {
  Sparkle24Filled,
  WeatherMoon20Regular,
  WeatherSunny20Regular,
} from "@fluentui/react-icons";

import { HealthCard } from "./components/HealthCard";
import { koyarwaDarkTheme, koyarwaLightTheme } from "./theme/koyarwaTheme";

const useStyles = makeStyles({
  shell: {
    minHeight: "100vh",
    backgroundColor: tokens.colorNeutralBackground2,
    color: tokens.colorNeutralForeground1,
    display: "flex",
    flexDirection: "column",
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    paddingInline: tokens.spacingHorizontalXXL,
    paddingBlock: tokens.spacingVerticalL,
    borderBottom: `1px solid ${tokens.colorNeutralStroke2}`,
    backgroundColor: tokens.colorNeutralBackground1,
  },
  brand: {
    display: "flex",
    alignItems: "center",
    columnGap: tokens.spacingHorizontalS,
    color: tokens.colorBrandForeground1,
  },
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    rowGap: tokens.spacingVerticalXXL,
    padding: tokens.spacingHorizontalXXL,
    textAlign: "center",
  },
  hero: {
    display: "flex",
    flexDirection: "column",
    rowGap: tokens.spacingVerticalS,
    maxWidth: "560px",
  },
});

function AppShell({ dark, onToggleTheme }) {
  const styles = useStyles();

  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <div className={styles.brand}>
          <Sparkle24Filled />
          <Title1>Koyarwa</Title1>
        </div>
        <Tooltip content={dark ? "Thème clair" : "Thème sombre"} relationship="label">
          <Button
            appearance="subtle"
            icon={dark ? <WeatherSunny20Regular /> : <WeatherMoon20Regular />}
            onClick={onToggleTheme}
            aria-label="Basculer le thème"
          />
        </Tooltip>
      </header>

      <main className={styles.main}>
        <div className={styles.hero}>
          <Title1>Bienvenue sur Koyarwa 👋</Title1>
          <Subtitle2>
            Projet de base : API FastAPI + client React et Fluent UI.
          </Subtitle2>
        </div>
        <HealthCard />
      </main>
    </div>
  );
}

export default function App() {
  const [dark, setDark] = useState(false);
  const theme = dark ? koyarwaDarkTheme : koyarwaLightTheme;

  return (
    <FluentProvider theme={theme}>
      <AppShell dark={dark} onToggleTheme={() => setDark((value) => !value)} />
    </FluentProvider>
  );
}
