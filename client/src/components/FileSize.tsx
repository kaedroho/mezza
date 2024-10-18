interface FileSizeProps {
  bytes: number;
}

export default function FileSize({ bytes }: FileSizeProps) {
  if (bytes < 1024) {
    return `${bytes} bytes`;
  }

  const kilobytes = bytes / 1024;

  if (kilobytes < 1024) {
    return `${kilobytes.toFixed(2)} KB`;
  }

  const megabytes = kilobytes / 1024;

  return `${megabytes.toFixed(2)} MB`;
}
