export interface Workspace {
  slug: string;
  name: string;
}

export interface FileAttributes {
  dimensions?: {
    width: number;
    height: number;
    unit: "pixels";
  },
  duration?: number,
}

export interface FileBlob {
  size: number;
  content_type: string;
  attributes: FileAttributes;
  download_url: string;
}

export interface File {
  id: number;
  name: string;
  source_blob: FileBlob;
  detail_url: string;
}
