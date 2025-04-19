import Box from "@mui/joy/Box";
import FileSize from "../components/FileSize";
import Layout from "../components/Layout";
import { File } from "../types";

interface FileDetailViewProps {
  file: File;
}

export default function FileDetailView({ file }: FileDetailViewProps) {
  return (
    <Layout title={file.name} noIndent>
      <Box
        sx={{
          display: "flex",
          flexFlow: "row nowrap",
          width: "100%",
          justifyContent: "center",
          my: 2,
          img: {
            maxWidth: "100%",
            height: "auto",
            maxHeight: "500px",
          },
          video: {
            maxWidth: "100%",
            height: "auto",
            maxHeight: "500px",
          },
        }}
      >
        {file.source_blob.content_type === "image/jpeg" && (
          <img src={file.source_blob.download_url} alt={file.name} />
        )}
        {file.source_blob.content_type === "video/mp4" && (
          <video src={file.source_blob.download_url} controls />
        )}
      </Box>
      <Box sx={{ mt: 2, px: 2 }}>
        <p>
          <b>Content type:</b> {file.source_blob.content_type}
        </p>
        <p>
          <b>Size:</b> <FileSize bytes={file.source_blob.size} />
        </p>
        {file.source_blob.attributes.dimensions && (
          <p>
            <b>Dimensions:</b> {file.source_blob.attributes.dimensions.width} x {file.source_blob.attributes.dimensions.height}
          </p>
        )}
        {file.source_blob.attributes.duration && (
          <p>
            <b>Duration:</b> {file.source_blob.attributes.duration} seconds
          </p>
        )}
      </Box>
    </Layout>
  );
}
