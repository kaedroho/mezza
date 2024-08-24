import { NavigationContext } from "@django-bridge/react";
import { Add } from "@mui/icons-material";
import Button from "@mui/joy/Button";
import React from "react";
import styled from "styled-components";
import Layout from "../components/Layout";
import ModalWindow from "../components/ModalWindow";
import { URLsContext } from "../contexts";
import { Project, Stage } from "../types";

const Kanban = styled.div`
  display: flex;
  flex-flow: row nowrap;
  flex-stretch: 1;
  gap: 20px;
  width: 100vw;
  overflow-x: auto;
  padding: 20px;
  flex-basis: 100%;
`;

const StageColumn = styled.div``;

const StageHeader = styled.div`
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  align-items: center;
  padding-left: 10px;

  > h2 {
    margin: 0;
    font-size: 1.2em;
  }
`;

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

interface ProjectsBoardViewProps {
  stages: Stage[];
  projects: Project[];
}

export default function ProjectsBoardView({
  stages,
  projects,
}: ProjectsBoardViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const urls = React.useContext(URLsContext);

  const projectsByStage = React.useMemo(() => {
    const projectsByStage: Record<string, Project[]> = {};

    projects.forEach((project) => {
      if (!projectsByStage[project.stage.slug]) {
        projectsByStage[project.stage.slug] = [];
      }

      projectsByStage[project.stage.slug].push(project);
    });

    return projectsByStage;
  }, [projects]);

  return (
    <Layout title="Projects">
      <Kanban>
        {stages.map((stage) => {
          const stageProjects = projectsByStage[stage.slug] || [];

          return (
            <StageColumn key={stage.slug}>
              <StageHeader>
                <h2>{stage.title}</h2>
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
                  New Project
                </Button>
              </StageHeader>
              <Projects>
                {stageProjects.map((project) => (
                  <ProjectCard key={project.id}>
                    <h2>{project.title}</h2>
                    <p>{project.description}</p>
                  </ProjectCard>
                ))}
              </Projects>
            </StageColumn>
          );
        })}
      </Kanban>
    </Layout>
  );
}
