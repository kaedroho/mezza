import { ReactElement } from "react";
import BlockNoteEditor from "../../components/widgets/BlockNoteEditor";
import { WidgetDef } from "./base";

export default class BlockNoteEditorDef implements WidgetDef {
  render(
    id: string,
    name: string,
    disabled: boolean,
    value: string,
  ): ReactElement {
    return (
      <BlockNoteEditor
        id={id}
        name={name}
        disabled={disabled}
        initialContent={JSON.parse(value || "[]]")}
      />
    );
  }
}
