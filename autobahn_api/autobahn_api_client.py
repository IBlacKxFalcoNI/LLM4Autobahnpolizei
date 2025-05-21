import requests
import json
import os
import yaml

class AutobahnApiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def _get(self, endpoint, params=None):
        """
        Internal helper method for GET requests.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving '{url}': {e}")
            return None

    def get_available_roads(self):
        """
        Retrieves the list of available highways.
        """
        return self._get("/")

    def get_roadworks(self, road_id):
        """
        Retrieves the current construction sites for a specific highway.
        """
        return self._get(f"/{road_id}/services/roadworks")

    def get_roadwork_details(self, roadwork_id):
        """
        Retrieves the details of a specific construction site.
        """
        return self._get(f"/details/roadworks/{roadwork_id}")

    def get_warnings(self, road_id):
        """
        Retrieves the latest traffic reports for a specific highway.
        """
        return self._get(f"/{road_id}/services/warning")

    def get_warning_details(self, warning_id):
        """
        Retrieves the details of a specific traffic report.
        """
        return self._get(f"/details/warning/{warning_id}")

    def get_closures(self, road_id):
        """
        Retrieves the current closures for a specific highway.
        """
        return self._get(f"/{road_id}/services/closure")

    def get_closure_details(self, closure_id):
        """
        Retrieves the details of a specific block.
        """
        return self._get(f"/details/closure/{closure_id}")
    
    def get_all_data(self):
        """
        Retrieves roadworks, warnings and closures for all highways.
        """
        roads = self.get_available_roads()
        roads_data = dict()
        for road_id in roads["roads"]:
            print(f"Fetching data for {road_id}...", end="", flush=True)
            roadworks = self.get_roadworks(road_id)
            warnings = self.get_warnings(road_id)
            closures = self.get_closures(road_id)
            road_dict = {**roadworks, **warnings, **closures}
            # roads_data.update(road_dict)
            roads_data[road_id] = road_dict
            
            print(f"done ({len(road_dict)} items).")

        return roads_data



if __name__ == "__main__":
    # for testing
    config_path = os.path.join(os.getcwd(), "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    base_url = config.get("autobahn_api_url")

    client = AutobahnApiClient(base_url)

    print("Available highways:")
    roads = client.get_available_roads()
    if roads:
        print(json.dumps(roads, indent=4, ensure_ascii=False))
    else:
        print("Couldn't retrieve any highways.")

    road_id_example = "A8"  # example highway for Stuttgart

    # print(f"\n Construction sites on the {road_id_example}:")
    # roadworks = client.get_roadworks(road_id_example)
    # if roadworks:
    #     print(json.dumps(roadworks, indent=4, ensure_ascii=False))
    # else:
    #     print(f"Could not retrieve any construction sites on the {road_id_example}.")

    # print(f"\nTraffic reports on the {road_id_example}:")
    # warnings = client.get_warnings(road_id_example)
    # if warnings:
    #     print(json.dumps(warnings, indent=4, ensure_ascii=False))
    # else:
    #     print(f"Could not retrieve any traffic reports on the {road_id_example}.")

    print(f"\nClosures on the {road_id_example}:")
    closures = client.get_closures(road_id_example)
    if closures:
        print(json.dumps(closures, indent=4, ensure_ascii=False))
    else:
        print(f"Could not retrieve any closures on the {road_id_example}.")