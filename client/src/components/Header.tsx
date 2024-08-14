import Sheet from "@mui/joy/Sheet";

import Typography from "@mui/joy/Typography";
import ColorSchemeToggle from "./ColorSchemeToggle";

export default function Header() {
  return (
    <Sheet
      sx={{
        display: "flex",
        flexFlow: "row nowrap",
        alignItems: "center",
        justifyContent: "space-between",
        top: 0,
        width: "100vw",
        height: "var(--Header-height)",
        px: 4,
        py: 2,
        gap: 1,
        borderBottom: "1px solid",
        borderColor: "background.level1",
        color: "var(--joy-palette-neutral-100)",
        backgroundColor: "var(--joy-palette-neutral-900)",
        "--joy-palette-text-primary": "var(--joy-palette-neutral-100)",
        "--joy-palette-text-icon": "var(--joy-palette-neutral-100)",
        "--joy-palette-neutral-outlinedBorder": "var(--joy-palette-neutral-700)",
        "--joy-palette-neutral-outlinedColor": "var(--joy-palette-neutral-200)",
        "--joy-palette-neutral-outlinedActiveBg": "var(--joy-palette-neutral-100)",
        "--joy-palette-neutral-outlinedHoverBg": "var(--joy-palette-neutral-800)",
        "--variant-outlinedActiveBg": "var(--joy-palette-neutral-700)",
      }}
    >
      <Typography level="title-lg" fontWeight="xl">
        CrowFlow
      </Typography>
      <ColorSchemeToggle sx={{ ml: "auto" }} />
    </Sheet>
  );
}
