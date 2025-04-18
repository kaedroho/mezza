import {
  DirtyFormContext,
  Link as DjangoBridgeLink,
  Message,
  MessagesContext,
  OverlayContext,
} from "@django-bridge/react";
import WarningRounded from "@mui/icons-material/WarningRounded";
import Box from "@mui/joy/Box";
import Breadcrumbs from "@mui/joy/Breadcrumbs";
import CssBaseline from "@mui/joy/CssBaseline";
import Link from "@mui/joy/Link";
import { CssVarsProvider } from "@mui/joy/styles";
import Typography from "@mui/joy/Typography";
import * as React from "react";
import styled, { keyframes } from "styled-components";

import ChevronRightRoundedIcon from "@mui/icons-material/ChevronRightRounded";

import Button from "@mui/joy/Button";
import Snackbar from "@mui/joy/Snackbar";
import Sidebar from "./Sidebar";

const slideDown = keyframes`
    from {
        margin-top: -50px;
    }

    to {
        margin-top: 0
    }
`;

const UnsavedChangesWarningWrapper = styled.div`
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  gap: 20px;
  padding: 15px 20px;
  color: #2e1f5e;
  font-size: 15px;
  font-weight: 400;
  margin-top: 0;
  background-color: #ffdadd;
  animation: ${slideDown} 0.5s ease;

  p {
    line-height: 19.5px;
  }

  strong {
    font-weight: 700;
  }
`;

interface LayoutProps {
  title: string;
  breadcrumb?: {
    label: string;
    href?: string;
  }[];
  renderHeaderButtons?: () => React.ReactNode;
  noIndent?: boolean;
}

export default function Layout({
  title,
  breadcrumb = [],
  renderHeaderButtons,
  noIndent = false,
  children,
}: React.PropsWithChildren<LayoutProps>) {
  const { overlay, requestClose } = React.useContext(OverlayContext);
  const { messages } = React.useContext(MessagesContext);
  const { unloadBlocked, confirmUnload } = React.useContext(DirtyFormContext);
  const [message, setMessage] = React.useState<Message | null>(null);

  React.useEffect(() => {
    if (messages.length > 0) {
      setMessage(messages[messages.length - 1]);
    }
  }, [messages]);

  if (overlay) {
    // The view is being rendered in an overlay, no need to render the menus or base CSS
    return (
      <>
        {unloadBlocked && (
          <UnsavedChangesWarningWrapper role="alert" aria-live="assertive">
            <WarningRounded />
            <p>
              <strong>You have unsaved changes.</strong> Please save or cancel
              before closing
            </p>
          </UnsavedChangesWarningWrapper>
        )}
        <Box
          sx={{
            px: { xs: 2, md: 6 },
            pt: { xs: 2, sm: 2, md: 3 },
            pb: { xs: 2, sm: 2, md: 3 },
          }}
        >
          <Box
            sx={{
              display: "flex",
              flexFlow: "row wrap",
              alignItems: "center",
            }}
          >
            <Typography level="h3" component="h2">
              {title}
            </Typography>
            <Box sx={{ ml: "auto" }}>
              {renderHeaderButtons && renderHeaderButtons()}
              {overlay && (
                <Button
                  type="button"
                  variant="outlined"
                  onClick={() => requestClose()}
                >
                  Close
                </Button>
              )}
            </Box>
          </Box>
          {children}
        </Box>
      </>
    );
  }

  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />

      <Box
        sx={{
          display: "flex",
          flexFlow: "row",
          height: "100vh",
          flexGrow: 1,
        }}
      >
        <Sidebar />
        <Box sx={{ display: "flex", flexFlow: "column nowrap", flexGrow: 1 }}>
          {unloadBlocked && (
            <UnsavedChangesWarningWrapper role="alert" aria-live="assertive">
              <WarningRounded />
              <p>
                <b>You have unsaved changes.</b> Please save your changes before
                leaving.
              </p>
              <Button
                type="button"
                size="sm"
                onClick={(e) => {
                  e.preventDefault();
                  confirmUnload();
                }}
              >
                Leave without saving
              </Button>
            </UnsavedChangesWarningWrapper>
          )}

          {message && (
            <Snackbar
              key={"html" in message ? message.html : message.text}
              anchorOrigin={{ vertical: "top", horizontal: "center" }}
              variant="solid"
              color={
                message.level === "error"
                  ? "danger"
                  : message.level === "warning"
                    ? "warning"
                    : "success"
              }
              autoHideDuration={5000}
              onClose={() => setMessage(null)}
              open
            >
              {"html" in message ? (
                <div dangerouslySetInnerHTML={{ __html: message.html }} />
              ) : (
                message.text
              )}
            </Snackbar>
          )}

          <Box
            component="main"
            className="MainContent"
            sx={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              minWidth: 0,
              overflow: "hidden auto",
              px: noIndent ? 0 : 2,
              backgroundColor: "var(--joy-palette-background-surface)",
            }}
          >
            <Box
              sx={{
                px: noIndent ? 2 : 0,
                backgroundColor: "var(--joy-palette-background-surface)",
              }}
            >
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Breadcrumbs
                  size="sm"
                  aria-label="breadcrumbs"
                  separator={<ChevronRightRoundedIcon />}
                  sx={{ pl: 0, minHeight: "34px" }}
                >
                  {breadcrumb.map(({ label, href }) =>
                    href ? (
                      <Link
                        component={DjangoBridgeLink}
                        underline="hover"
                        href={href}
                        fontSize={12}
                        fontWeight={500}
                        key={href}
                      >
                        {label}
                      </Link>
                    ) : (
                      <Typography
                        color="primary"
                        fontWeight={500}
                        fontSize={12}
                      >
                        {label}
                      </Typography>
                    ),
                  )}
                </Breadcrumbs>
              </Box>
              <Box
                sx={{
                  display: "flex",
                  mb: 1,
                  gap: 2,
                  flexDirection: { xs: "column", sm: "row" },
                  alignItems: { xs: "start", sm: "center" },
                  flexWrap: "wrap",
                }}
              >
                <Typography level="h3" component="h1">
                  {title}
                </Typography>
                <Box sx={{ ml: "auto" }}>
                  {renderHeaderButtons && renderHeaderButtons()}
                </Box>
              </Box>
            </Box>
            {children}
          </Box>
        </Box>
      </Box>
    </CssVarsProvider>
  );
}
