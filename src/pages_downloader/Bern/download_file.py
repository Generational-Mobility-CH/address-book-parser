from pathlib import Path

import requests


def download_file(file_download_url: str, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(file_download_url)
        response.raise_for_status()
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
