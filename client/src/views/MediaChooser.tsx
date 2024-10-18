import { OverlayContext } from "@django-bridge/react";
import React from "react";
import AssetList from "../components/AssetList";
import Layout from "../components/Layout";
import { CSRFTokenContext } from "../contexts";
import { Asset } from "../types";

interface MediaChooserViewProps {
  action_url: string;
  assets: Asset[];
}

export default function MediaChooserView({
  action_url,
  assets,
}: MediaChooserViewProps) {
  const { requestClose } = React.useContext(OverlayContext);
  const csrf_token = React.useContext(CSRFTokenContext);

  return (
    <Layout title="Choose Asset">
      <AssetList
        assets={assets}
        onClickAsset={(asset) => {
          fetch(action_url, {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "X-CSRFToken": csrf_token,
            },
            body: new URLSearchParams({
              asset_id: asset.id.toString(),
            }),
          }).then(() => requestClose());
        }}
      />
    </Layout>
  );
}
