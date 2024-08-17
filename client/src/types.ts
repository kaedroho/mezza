export interface Stage {
  id: number;
  title: string;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  stage: Stage;
  edit_url: string;
}
