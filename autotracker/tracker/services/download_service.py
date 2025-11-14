from __future__ import annotations
import os
from pathlib import Path
import requests

from tracker.models import Episode


def download_episode_file(episode: Episode, download_dir: str = 'downloads') -> str:
    os.makedirs(download_dir, exist_ok=True)
    local_filename = f"{episode.id}_{os.path.basename(episode.download_url.split('?')[0]) or 'episode.dat'}"
    file_path = Path(download_dir) / local_filename

    response = requests.get(episode.download_url, stream=True, timeout=60)
    response.raise_for_status()
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    episode.downloaded_file_path = str(file_path)
    episode.is_downloaded = True
    episode.save(update_fields=['downloaded_file_path', 'is_downloaded'])
    return str(file_path)
