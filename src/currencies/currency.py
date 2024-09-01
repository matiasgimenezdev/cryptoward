from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from typing import Union, Optional


@dataclass
class Currency:
    name: str
    code: str
    endpoint: str
    index: int

    def __init__(self, name: str, code: str, endpoint: str, index: int) -> None:
        self.name = name
        self.code = code
        self.endpoint = endpoint
        self.index = index

    @classmethod
    def get_exchange_rate(cls) -> float:
        response = requests.get("https://api.bluelytics.com.ar/v2/latest")
        response.raise_for_status()
        exchange_data = response.json()
        exchange_rate = exchange_data["blue"]["value_sell"]
        return exchange_rate

    def fetch_price(
        self, class_selector: str = "sc-65e7f566-0 clvjgF base-text"
    ) -> Optional[str]:
        try:
            response = requests.get(self.endpoint)
            html_content = response.text
            page = BeautifulSoup(html_content, "html.parser")
            element: Union[Tag, None, NavigableString] = page.find(
                class_=class_selector
            )

            if element is None:
                return None

            price = element.get_text().split("$")[1].replace(",", "")
            return price
        except Exception:
            raise requests.RequestException(f"Error fetching data from {self.endpoint}")
