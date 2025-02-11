import requests
import os

import voeventparse

dataverse_url = "https://opendata.km3net.de"
dataset_doi = "doi:10.5072/FK2/JW72C9"
output_directory = "../"

vo_filepath = "../data/event/KM3-230213A_voevent.xml"

def download_from_odc(api_token=None, output_dir = ""):
    """
    Download all files from a Dataverse dataset while preserving the original folder structure.
    
    :param dataverse_url: Base URL of the Dataverse repository (e.g., https://demo.dataverse.org)
    :param dataset_doi: DOI or persistent identifier of the dataset (e.g., "doi:10.7910/DVN/TJCLKP")
    :param api_token: Optional API token if authentication is required
    :param output_dir: Directory to save downloaded files
    """

    if not output_dir:
        output_dir = output_directory
        
    headers = {}
    if api_token:
        headers["X-Dataverse-key"] = api_token

    # Construct the dataset API URL
    dataset_url = f"{dataverse_url}/api/datasets/:persistentId/?persistentId={dataset_doi}"
    response = requests.get(dataset_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve dataset metadata: {response.status_code}")
        return
    
    data = response.json()
    files = data.get("data", {}).get("latestVersion", {}).get("files", [])
    
    if not files:
        print("No files found in the dataset.")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    for file in files:
        file_id = file["dataFile"]["id"]
        file_name = file["dataFile"]["filename"]
        file_path = file.get("directoryLabel", "")
        full_file_path = os.path.join(output_dir, file_path, file_name)
        file_url = f"{dataverse_url}/api/access/datafile/{file_id}"
        
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        if os.path.exists(full_file_path):
            print(f"Skipping {full_file_path}, already exists.")
            continue

        print(f"Downloading {full_file_path}...")
        file_response = requests.get(file_url, headers=headers, stream=True)
        
        if file_response.status_code == 200:
            with open(full_file_path, "wb") as f:
                for chunk in file_response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"Saved {full_file_path}")
        else:
            print(f"Failed to download {file_name}: {file_response.status_code}")

def get_event(voevent_filepath = ""):
    """Get basic event data from VOEvent, optionally using filepath."""

    if not voevent_filepath:
        voevent_filepath = vo_filepath
    with open(voevent_filepath, 'rb') as f:
        voevent = voeventparse.load(f)

    return voevent
