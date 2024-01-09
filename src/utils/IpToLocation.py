import json
import requests


class IpToLocation:
    base_url = "http://ip-api.com/json/"

    @classmethod
    def get_ip_info(cls, ip):
        # Obtain JSON data from the API
        json_data = cls.get_json_from_api(ip)
        if json_data:
            # Retrieve the values associated with the keys "regionName" and "zip"
            region_name = cls.search_value_in_json(json_data, "regionName")
            zip_code = cls.search_value_in_json(json_data, "zip")

            # Return a tuple containing both values
            return region_name, zip_code
        return None

    @classmethod
    def get_json_from_api(cls, ip):
        try:
            # Make a GET request to the API with the provided IP address
            response = requests.get(cls.base_url + ip)
            response.raise_for_status()  # Raise an exception for non-successful status codes

            # Return the JSON data from the response
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")
        return None

    @staticmethod
    def search_value_in_json(json_data, key):
        # Check if the key exists in the JSON data
        if key in json_data:
            # Return the value associated with the specified key
            return json_data[key]
        else:
            # Print an error message if the key is not found in the JSON
            print(f"Key '{key}' not found in JSON.")
            return None

    @classmethod
    def get_complete_ip_info_json_string(cls, ip):
        # Obtain JSON data from the API
        json_data = cls.get_json_from_api(ip)

        return json.dumps(json_data, indent=2)
