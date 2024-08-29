import {
  Link as DjangoBridgeLink,
  NavigationContext,
} from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Button from "@mui/joy/Button";
import Link from "@mui/joy/Link";
import React from "react";
import styled from "styled-components";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { URLsContext } from "../contexts";
import { Project, Stage } from "../types";

const Projects = styled.ul`
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  list-style: none;
  padding: 0;
`;

const ProjectCard = styled.li`
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

interface ProjectsStageIndexViewProps {
  stage: Stage;
  projects: Project[];
}

export default function ProjectsStageIndexView({
  stage,
  projects,
}: ProjectsStageIndexViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const urls = React.useContext(URLsContext);

  return (
    <Layout
      title={stage.title}
      renderHeaderButtons={() => (
        <Button
          variant="plain"
          color="primary"
          size="sm"
          startDecorator={<Add />}
          onClick={() =>
            openOverlay(
              urls.projects_create.replace("stage", stage.slug),
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
      <Projects>
        {projects.map((project) => (
          <ProjectCard key={project.id}>
            <Link component={DjangoBridgeLink} href={project.detail_url}>
              <h2>{project.title}</h2>
              <p>{project.description}</p>
            </Link>
          </ProjectCard>
        ))}
      </Projects>
    </Layout>
  );
}
