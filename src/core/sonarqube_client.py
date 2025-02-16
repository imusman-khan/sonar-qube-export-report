import requests
from typing import Dict, Any
from src.core.logger import logger


class SonarQubeClient:
    """
    A client to interact with the SonarQube API.

    This class provides methods to make authenticated requests to the SonarQube API. It handles the base URL and
    authentication token, and logs errors that occur during API requests.

    Attributes:
        base_url (str): The base URL of the SonarQube server.
        headers (Dict[str, str]): The headers for authenticated requests, including the Authorization token.
    """

    def __init__(self, base_url: str, token: str):
        """
        Initializes the SonarQubeClient with the base URL and authentication token.

        Args:
            base_url (str): The base URL of the SonarQube server.
            token (str): The authentication token for accessing the SonarQube API.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Makes a GET request to the specified SonarQube API endpoint.

        Args:
            endpoint (str): The API endpoint to request.
            params (Dict[str, Any], optional): The query parameters to include in the request. Defaults to None.

        Returns:
            Dict[str, Any]: The JSON response from the API, or an empty dictionary if an error occurs.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return {}
