import { ReactElement } from "react";
import TextArea from "../../components/widgets/TextArea";
import { WidgetDef } from "./base";

export default class TextAreaDef implements WidgetDef {
  minRows: 2;

  constructor(minRows: TextAreaDef["minRows"]) {
    this.minRows = minRows;
  }

  render(
    id: string,
    name: string,
    disabled: boolean,
    value: string,
  ): ReactElement {
    return (
      <TextArea
        id={id}
        minRows={this.minRows}
        name={name}
        defaultValue={value}
        disabled={disabled}
      />
    );
  }
}
