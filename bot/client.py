import hashlib
import hmac
import time
import urllib.parse
from typing import Any

import requests

from .logging_config import setup_logging

logger = setup_logging().getChild("client")

BASE_URL = "https://testnet.binance.vision"
TIMEOUT = 10  # seconds


class BinanceAPIError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error {code}: {message}")


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, endpoint: str, params: dict = None) -> Any:
        url = BASE_URL + endpoint
        params = params or {}
        signed_params = self._sign(params)

        logger.debug("REQUEST  %s %s | params: %s", method.upper(), url, signed_params)

        try:
            response = self.session.request(
                method, url, params=signed_params, timeout=TIMEOUT
            )
        except requests.exceptions.ConnectionError as e:
            logger.error("Network connection error: %s", e)
            raise ConnectionError(f"Could not connect to Binance Testnet: {e}") from e
        except requests.exceptions.Timeout:
            logger.error("Request timed out after %ss", TIMEOUT)
            raise TimeoutError("Request to Binance Testnet timed out.")

        logger.debug(
            "RESPONSE %s %s | status: %s | body: %s",
            method.upper(),
            url,
            response.status_code,
            response.text[:500],
        )

        data = response.json()

        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            logger.error("API error: %s", data)
            raise BinanceAPIError(data["code"], data.get("msg", "Unknown error"))

        return data

    def post(self, endpoint: str, params: dict = None) -> Any:
        return self._request("POST", endpoint, params)

    def get(self, endpoint: str, params: dict = None) -> Any:
        return self._request("GET", endpoint, params)
