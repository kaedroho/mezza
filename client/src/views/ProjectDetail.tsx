import Layout from "../components/Layout";
import { Project } from "../types";

interface ProjectDetailViewProps {
  project: Project;
}

export default function ProjectDetailView({ project }: ProjectDetailViewProps) {
  return <Layout title={project.title}></Layout>;
}
