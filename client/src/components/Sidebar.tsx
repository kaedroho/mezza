import DashboardRoundedIcon from "@mui/icons-material/DashboardRounded";
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
import { FileDownload } from "@mui/icons-material";
import { StagesContext, URLsContext } from "../contexts";
import { closeSidebar } from "../utils";
import ColorSchemeToggle from "./ColorSchemeToggle";

export default function Sidebar() {
  const { navigate: doNavigate } = React.useContext(NavigationContext);
  const urls = React.useContext(URLsContext);
  const stages = React.useContext(StagesContext);

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
        // transform: {
        //   xs: "translateX(calc(100% * (var(--SideNavigation-slideIn, 0) - 1)))",
        //   md: "none",
        // },
        pt: {
          md: 2,
        },
        transition: "transform 0.4s, width 0.4s",
        width: "var(--Sidebar-width)",
        top: "var(--Header-height)",
        p: 2,
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
            "--Sidebar-width": "200px",
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
            gap: 1,
            "--List-nestedInsetStart": "30px",
            "--ListItem-radius": (theme) => theme.vars.radius.sm,
          }}
        >
          <ListItem sx={{ px: 0, pb: 1 }}>
            <Typography
              level="title-lg"
              fontWeight="xl"
              sx={{ color: "#6a44f6" }}
            >
              Mezza Studio
            </Typography>
            <ColorSchemeToggle sx={{ ml: "auto" }} />
          </ListItem>

          <ListItem>
            <ListItemButton onClick={() => navigate(urls.projects_index)}>
              <DashboardRoundedIcon />
              <ListItemContent>
                <Typography level="title-sm">Projects</Typography>
              </ListItemContent>
            </ListItemButton>
          </ListItem>

          {stages.map((stage) => (
            <ListItem key={stage.slug}>
              <ListItemButton onClick={() => navigate(stage.projects_url)}>
                <ListItemContent>
                  <Typography level="title-sm">{stage.title}</Typography>
                </ListItemContent>
              </ListItemButton>
            </ListItem>
          ))}

          <ListItem>
            <ListItemButton onClick={() => navigate("/posts/")}>
              <FileDownload />
              <ListItemContent>
                <Typography level="title-sm">Assets</Typography>
              </ListItemContent>
            </ListItemButton>
          </ListItem>

          {/* <ListItem>
            <Button
              variant="plain"
              color="primary"
              size="sm"
              startDecorator={<Add />}
            >
              New Board
            </Button>
          </ListItem>
          <ListItem>
            <Typography fontWeight={600}>Publishing</Typography>
          </ListItem>
          <ListItem>
            <ListItemButton onClick={() => navigate("/")}>
              <CalendarMonth />
              <ListItemContent>
                <Typography level="title-sm">Calendar</Typography>
              </ListItemContent>
            </ListItemButton>
          </ListItem> */}
        </List>
      </Box>
      <Divider />
    </Sheet>
  );
}
