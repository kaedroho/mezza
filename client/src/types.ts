export interface Workspace {
  slug: string;
  name: string;
}


export interface File {
  id: number;
  name: string;
  size: number;
  content_type: string;
  attributes: Record<string, any>;
  download_url: string;
  detail_url: string;
}
