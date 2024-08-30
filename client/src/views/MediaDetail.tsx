import Layout from "../components/Layout";
import { Asset } from "../types";

interface MediaDetailViewProps {
  asset: Asset;
}

export default function MediaDetailView({ asset }: MediaDetailViewProps) {
  return (
    <Layout title={asset.title} noIndent>
      {JSON.stringify(asset, undefined, 2)}
    </Layout>
  );
}
