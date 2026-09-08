import { useCallback, useEffect, useState } from "react";
import {
  Badge,
  Body1,
  Button,
  Caption1,
  Card,
  CardHeader,
  Spinner,
  makeStyles,
  tokens,
} from "@fluentui/react-components";
import {
  ArrowClockwise20Regular,
  CheckmarkCircle16Filled,
  ErrorCircle16Filled,
  Server24Regular,
} from "@fluentui/react-icons";

import { getHealth } from "../api/client";

const useStyles = makeStyles({
  card: {
    maxWidth: "420px",
    width: "100%",
  },
  body: {
    display: "flex",
    flexDirection: "column",
    rowGap: tokens.spacingVerticalM,
  },
  statusRow: {
    display: "flex",
    alignItems: "center",
    columnGap: tokens.spacingHorizontalS,
  },
  error: {
    color: tokens.colorPaletteRedForeground1,
    wordBreak: "break-word",
  },
});

export function HealthCard() {
  const styles = useStyles();
  const [state, setState] = useState({ phase: "loading" });

  const check = useCallback(async () => {
    setState({ phase: "loading" });
    try {
      const data = await getHealth();
      setState({ phase: "ok", data });
    } catch (err) {
      setState({ phase: "error", message: String(err?.message ?? err) });
    }
  }, []);

  useEffect(() => {
    check();
  }, [check]);

  return (
    <Card className={styles.card}>
      <CardHeader
        image={<Server24Regular />}
        header={<Body1><b>API backend</b></Body1>}
        description={<Caption1>GET /api/v1/health</Caption1>}
      />

      <div className={styles.body}>
        {state.phase === "loading" && (
          <Spinner size="tiny" label="Vérification…" labelPosition="after" />
        )}

        {state.phase === "ok" && (
          <div className={styles.statusRow}>
            <Badge appearance="filled" color="success" icon={<CheckmarkCircle16Filled />}>
              {state.data.status}
            </Badge>
            <Caption1>version {state.data.version}</Caption1>
          </div>
        )}

        {state.phase === "error" && (
          <div className={styles.statusRow}>
            <Badge appearance="filled" color="danger" icon={<ErrorCircle16Filled />}>
              injoignable
            </Badge>
            <Caption1 className={styles.error}>{state.message}</Caption1>
          </div>
        )}

        <div>
          <Button
            appearance="secondary"
            icon={<ArrowClockwise20Regular />}
            onClick={check}
            disabled={state.phase === "loading"}
          >
            Réessayer
          </Button>
        </div>
      </div>
    </Card>
  );
}
