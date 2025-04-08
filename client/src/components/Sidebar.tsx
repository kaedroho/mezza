import Box from "@mui/joy/Box";
import Divider from "@mui/joy/Divider";
import GlobalStyles from "@mui/joy/GlobalStyles";
import List from "@mui/joy/List";
import ListItem from "@mui/joy/ListItem";
import ListItemButton, { listItemButtonClasses } from "@mui/joy/ListItemButton";
import ListItemContent from "@mui/joy/ListItemContent";
import Sheet from "@mui/joy/Sheet";
import Typography from "@mui/joy/Typography";
import * as React from "react";

import { NavigationContext } from "@django-bridge/react";
import { URLsContext, WorkspacesContext } from "../contexts";
import { closeSidebar } from "../utils";
import ColorSchemeToggle from "./ColorSchemeToggle";

export default function Sidebar() {
  const { navigate: doNavigate } = React.useContext(NavigationContext);
  const { current, workspaces } = React.useContext(WorkspacesContext);
  const [navigatingTo, setNavigatingTo] = React.useState<string | null>(null);
  const workspace = workspaces.find((s) => s.slug === current);
  const urls = React.useContext(URLsContext);

  const navigate = React.useCallback(
    (path: string) => {
      closeSidebar();
      doNavigate(path);
    },
    [doNavigate],
  );

  return (
    <Sheet
      className="Sidebar"
      sx={{
        pt: {
          md: 2,
        },
        transition: "transform 0.4s, width 0.4s",
        width: "var(--Sidebar-width)",
        top: "var(--Header-height)",
        flexShrink: 0,
        display: "flex",
        flexDirection: "column",
        gap: 2,
        borderRight: "1px solid",
        borderColor: "divider",
      }}
    >
      <GlobalStyles
        styles={() => ({
          ":root": {
            "--Sidebar-width": "240px",
          },
        })}
      />
      <Box
        className="Sidebar-overlay"
        sx={{
          position: "fixed",
          zIndex: 9998,
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
          opacity: "var(--SideNavigation-slideIn)",
          backgroundColor: "var(--joy-palette-background-backdrop)",
          transition: "opacity 0.4s",
          transform: {
            xs: "translateX(calc(100% * (var(--SideNavigation-slideIn, 0) - 1) + var(--SideNavigation-slideIn, 0) * var(--Sidebar-width, 0px)))",
            lg: "translateX(-100%)",
          },
        }}
        onClick={() => closeSidebar()}
      />
      <Box
        sx={{
          minHeight: 0,
          overflow: "hidden auto",
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          [`& .${listItemButtonClasses.root}`]: {
            gap: 1.5,
          },
        }}
      >
        <List
          size="sm"
          sx={{
            "--List-nestedInsetStart": "30px",
            "--ListItem-radius": (theme) => theme.vars.radius.sm,
          }}
        >
          <ListItem sx={{ px: 2, pb: 1 }}>
            <Typography level="title-md" fontWeight="xl">
              {workspace?.name || "Mezza"}
            </Typography>
            <ColorSchemeToggle sx={{ ml: "auto" }} />
          </ListItem>

          <ListItem>
            <ListItemButton
              sx={{ borderRadius: 0, py: 1 }}
              onClick={() => {
                navigate(urls.file_index);
                setNavigatingTo(urls.file_index);
              }}
              selected={(navigatingTo || window.location.pathname).startsWith(
                urls.file_index,
              )}
            >
              <ListItemContent>
                <Typography level="title-sm">Files</Typography>
              </ListItemContent>
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
      <Divider />
    </Sheet>
  );
}
