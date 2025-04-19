export interface Workspace {
  slug: string;
  name: string;
}

export interface FileBlob {
  size: number;
  content_type: string;
  attributes: Record<string, any>;
  download_url: string;
}

export interface File {
  id: number;
  name: string;
  source_blob: FileBlob;
  detail_url: string;
}
