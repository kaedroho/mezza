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
