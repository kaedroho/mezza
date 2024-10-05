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
import { URLsContext } from "../contexts";
import { Project } from "../types";

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

interface ProjectsListingViewProps {
  projects: Project[];
}

export default function ProjectsListingView({
  projects,
}: ProjectsListingViewProps) {
  const { navigate } = React.useContext(NavigationContext);
  const urls = React.useContext(URLsContext);

  return (
    <Layout
      title="Projects"
      renderHeaderButtons={() => (
        <Button
          variant="plain"
          color="primary"
          size="sm"
          startDecorator={<Add />}
          onClick={() => navigate(urls.projects_create)}
        >
          New Project
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
