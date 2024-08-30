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
  asset_upload_url: string;
}

export interface Idea {
  id: number;
  title: string;
  description: string;
  start_production_url: string;
}

export interface Asset {
  id: number;
  title: string;
  detail_url: string;
}
