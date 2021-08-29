"""Http Request Executor."""

import requests
import logging
from config.config_loader import load_env_variable

LOG = logging.getLogger(__name__)

class HttpRequestExecutor:
    """HttpRequestExecutor class provides the flexibility to execute create, update, put and delete requests and returns a response."""

    def get_url(self, path: str) -> str:
        """Get the environment applicable API URL.
        
        Args:
            :param path: Absolute API path

        Returns:
            str: absolute URL
        """
        LOG.debug("Building URL")
        base_uri = load_env_variable('uri')
        return base_uri + path


    def get_api(self, path: str, params) -> requests.Response:
        """Send a GET (read) API request.

        Args:
            :param path: API URL path
            :param params: Headers

        Returns:
            Response: Response to the request
        """
        url = self.get_url(path)
        LOG.debug("url : " + url)
        LOG.debug("Executing Get requests")
        return requests.get(url, params=params)


    def post_api(self, path: str, body, params="") -> requests.Response:
        """Send a POST (create) API request.

        parameters:
            :param path: API URL path
            :param body: JSON payload
            :param params: Query parameters


        Returns:
            Response: Response to the request
        """
        url = self.get_url(path)
        LOG.debug("url : " + url)
        LOG.debug("Executing POST requests")
        return requests.post(url, json=body, params=params)


    def put_api(self, path: str, body, params="") -> requests.Response:
        """Send a PUT (update) API request.

        parameters:
            :param path: API URL path
            :param body: JSON payload
            :param params: Query parameters

        Returns:
            Response: Response to the request
        """
        url = self.get_url(path)
        LOG.debug("url : " + url)
        LOG.debug("Executing PUT requests")
        return requests.post(url, json=body, params=params)


    def delete_api(self, path: str) -> requests.Response:
        """Send a DELETE API request.

        parameters:
            :param path: API URL path

        Returns:
            Response: Response to the request
        """
        LOG.debug("Executing DELETE requests")
        url = self.get_url(path)
        return requests.delete(url)
