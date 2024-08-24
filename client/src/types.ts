export interface Stage {
  slug: string;
  title: string;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  stage: Stage;
  detail_url: string;
}

export interface Idea {
  id: number;
  title: string;
  description: string;
  start_production_url: string;
}

export interface File {
  id: number;
  title: string;
}
