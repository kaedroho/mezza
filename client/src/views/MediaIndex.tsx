import React from "react";
import styled from "styled-components";
import AddPhotoAlternateIcon from "@mui/icons-material/AddPhotoAlternate";
import Button from "@mui/joy/Button";

import Layout from "../components/Layout";
import { Link, NavigationContext } from "@django-bridge/react";
import ModalWindow from "../components/ModalWindow";

const MediaAssetListing = styled.ul`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(125px, 1fr));
  grid-gap: 20px;
  list-style: none;
  margin: 20px;

  li {
    display: flex;
    flex-flow: column;
    align-items: center;
    justify-content: center;
  }

  figure {
    display: flex;
    flex-flow: column;
    align-items: center;
  }

  figcaption {
    margin-top: 10px;
  }
`;

interface MediaIndexViewProps {
  type: string;
  types: {
    name: string;
    url: string;
  }[];
  files: {
    id: number;
    title: string;
    edit_url: string;
    thumbnail_url: string | null;
  }[];
}

export default function MediaIndexView({ types, files }: MediaIndexViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);

  return (
    <Layout
      title="Media"
      breadcrumb={[{ label: "" }]}
      renderHeaderButtons={() => (
        <Button
          color="primary"
          startDecorator={<AddPhotoAlternateIcon />}
          size="sm"
          onClick={() =>
            openOverlay(
              "/media/add-image/",
              (content) => (
                <ModalWindow slideout="right">{content}</ModalWindow>
              ),
              {
                onClose: () => {
                  // Refresh props so new image pops up in listing
                  refreshProps();
                },
              },
            )
          }
        >
          Add Image
        </Button>
      )}
    >
      <ul>
        {types.map((type) => (
          <li key={type.name}>
            <Link href={type.url}>{type.name}</Link>
          </li>
        ))}
      </ul>
      <MediaAssetListing>
        {files.map((file) => (
          <li key={file.id}>
            <Link href={file.edit_url}>
              <figure>
                <img src={file.thumbnail_url || "#"} alt={file.title} />
                <figcaption>{file.title}</figcaption>
              </figure>
            </Link>
          </li>
        ))}
      </MediaAssetListing>
    </Layout>
  );
}
