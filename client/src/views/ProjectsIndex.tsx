import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Button from "@mui/joy/Button";
import React from "react";
import styled from "styled-components";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { URLsContext } from "../contexts";
import { Project } from "../types";

const Cards = styled.ul`
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  list-style: none;
  padding: 0;
`;

const Card = styled.li`
  background-color: var(--joy-palette-background-paper);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;

  h2 {
    font-size: 1.25em;
    margin-bottom: 1em;
  }

  p {
    line-height: 1.5em;
  }
`;

interface ProjectsIndexViewProps {
  projects: Project[];
}

export default function ProjectsIndexView({
  projects,
}: ProjectsIndexViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const urls = React.useContext(URLsContext);

  return (
    <Layout
      title="Projects"
      renderHeaderButtons={() => {
        return (
          <Button
            variant="soft"
            color="primary"
            size="sm"
            startDecorator={<Add />}
            onClick={() =>
              openOverlay(
                urls.projects_create,
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
        );
      }}
    >
      <Cards>
        {projects.map((project) => (
          <Card key={project.id}>
            <h2>{project.title}</h2>
            <p>{project.description}</p>
          </Card>
        ))}
      </Cards>
    </Layout>
  );
}
