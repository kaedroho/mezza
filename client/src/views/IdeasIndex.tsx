import { NavigationContext } from "@django-bridge/react";
import { Add, Start } from "@mui/icons-material";
import Button from "@mui/joy/Button";
import React from "react";
import styled from "styled-components";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { URLsContext } from "../contexts";
import { Idea } from "../types";

const IdeaList = styled.ul`
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  list-style: none;
  padding: 0;
`;

const IdeaCard = styled.li`
  background-color: var(--joy-palette-background-paper);
  border-radius: 8px;
  border: 1px solid var(--joy-palette-neutral-outlinedBorder);
  padding: 10px;

  h2 {
    font-size: 1.25em;
    margin-bottom: 1em;
  }

  p {
    line-height: 1.5em;
  }
`;

interface IdeasIndexProps {
  ideas: Idea[];
}

export default function IdeasIndex({ ideas }: IdeasIndexProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const urls = React.useContext(URLsContext);

  return (
    <Layout
      title="Ideas"
      renderHeaderButtons={() => (
        <Button
          variant="plain"
          color="primary"
          size="sm"
          startDecorator={<Add />}
          onClick={() =>
            openOverlay(
              urls.ideas_create,
              (content) => <ModalWindow>{content}</ModalWindow>,
              {
                onClose: () => {
                  // Refresh props so new post pops up in listing
                  refreshProps();
                },
              },
            )
          }
        >
          New
        </Button>
      )}
    >
      <IdeaList>
        {ideas.map((idea) => (
          <IdeaCard key={idea.id}>
            <h2>{idea.title}</h2>
            <p>{idea.description}</p>
            <Button
              variant="solid"
              color="primary"
              size="sm"
              endDecorator={<Start />}
              onClick={() =>
                openOverlay(
                  idea.start_production_url,
                  (content) => (
                    <ModalWindow slideout="right">{content}</ModalWindow>
                  ),
                  {
                    onClose: () => {
                      // Refresh props so new post pops up in listing
                      refreshProps();
                    },
                  },
                )
              }
            >
              Start Production
            </Button>
          </IdeaCard>
        ))}
      </IdeaList>
    </Layout>
  );
}
