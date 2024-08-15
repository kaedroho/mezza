import { DirtyFormMarker } from "@django-bridge/react";
import Input from "@mui/joy/Input";
import InputProps from "@mui/joy/Input/InputProps";
import { SxProps } from "@mui/joy/styles/types";
import React from "react";

export interface TextInputProps extends InputProps {
  avariant: "default" | "large";
}

export default function TextInput({
  avariant,
  onChange: originalOnChange,
  ...props
}: TextInputProps) {
  const [dirty, setDirty] = React.useState(false);

  let sx: SxProps = props.sx || {};
  if (avariant === "large") {
    sx = {
      ...sx,
      p: 1,
      px: 2,
      boxShadow: "none",
      background: "none",
      fontSize: "1.5rem",
      fontWeight: 600,
    };
  }

  const onChange = React.useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setDirty(true);

      if (originalOnChange) {
        originalOnChange(e);
      }
    },
    [originalOnChange],
  );

  return (
    <>
      {dirty && <DirtyFormMarker />}
      <Input {...props} sx={sx} onChange={onChange} />
    </>
  );
}
