import { DirtyFormMarker } from "@django-bridge/react";
import Textarea, { TextareaProps } from "@mui/joy/Textarea";
import React from "react";

export default function TextArea({
  onChange: originalOnChange,
  ...props
}: TextareaProps) {
  const [dirty, setDirty] = React.useState(false);

  const onChange = React.useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
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
      <Textarea {...props} onChange={onChange} />
    </>
  );
}
