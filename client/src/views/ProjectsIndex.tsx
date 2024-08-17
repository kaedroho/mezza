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
`;

const StageColumn = styled.div`
  border-radius: 8px;
  padding: 10px;
  border: 1px solid var(--joy-palette-neutral-outlinedBorder);

  > h2 {
    margin-top: 0;
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

interface ProjectsIndexViewProps {
  stages: Stage[];
  projects: Project[];
}

export default function ProjectsIndexView({
  projects,
}: ProjectsIndexViewProps) {
  const { openOverlay, refreshProps } = React.useContext(NavigationContext);
  const urls = React.useContext(URLsContext);

  const projectsByStage = React.useMemo(() => {
    const projectsByStage: Record<number, Project[]> = {};

    projects.forEach((project) => {
      if (!projectsByStage[project.stage.id]) {
        projectsByStage[project.stage.id] = [];
      }

      projectsByStage[project.stage.id].push(project);
    });

    return projectsByStage;
  }, [projects]);

  return (
    <Layout title="Projects">
      <Kanban>
        {Object.keys(projectsByStage).map((stageId) => {
          const stageProjects = projectsByStage[parseInt(stageId)];

          return (
            <StageColumn key={stageId}>
              <h2>{stageProjects[0].stage.title}</h2>
              <Button
                variant="soft"
                color="primary"
                size="sm"
                startDecorator={<Add />}
                onClick={() =>
                  openOverlay(
                    urls.projects_create
                      .replace("flow", "video")
                      .replace("stage", stageId),
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
