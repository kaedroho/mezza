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

export interface File {
  id: number;
  name: string;
  download_url: string;
  size: number;
  file_type: string;
  thumbnail: {
    type: "image" | "video";
    src: string;
  };
}

export interface ImageFile extends File {
  width: number;
  height: number;
}

export interface AssetBase {
  id: number;
  title: string;
  detail_url: string;
}

export interface ImageAsset extends AssetBase {
  type: "image";
  file: ImageFile;
}

export interface VideoAsset extends AssetBase {
  type: "video";
  file: File;
}

export interface AudioAsset extends AssetBase {
  type: "audio";
  file: File;
}

export interface DocumentAsset extends AssetBase {
  type: "document";
  file: File;
}

export type Asset = ImageAsset | VideoAsset | AudioAsset | DocumentAsset;
