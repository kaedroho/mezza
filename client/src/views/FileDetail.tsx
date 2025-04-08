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
        {file.content_type === "image/jpeg" && (
          <img src={file.download_url} alt={file.name} />
        )}
        {file.content_type === "video/mp4" && (
          <video src={file.download_url} controls />
        )}
      </Box>
      <Box sx={{ mt: 2, px: 2 }}>
        <p>
          <b>Content type:</b> {file.content_type}
        </p>
        <p>
          <b>Size:</b> <FileSize bytes={file.size} />
        </p>
        {file.content_type === "image/jpeg" && (
          <p>
            <b>Dimensions:</b> {file.attributes["width"]} x {file.attributes["height"]}
          </p>
        )}
      </Box>
    </Layout>
  );
}
