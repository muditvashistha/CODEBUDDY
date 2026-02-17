import requests
from bs4 import BeautifulSoup

def fetch_clean_html(url: str) -> str:
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        
        for tag in soup(["script"]):
            tag.decompose()

        
        for img in soup.find_all("img"):
            img["src"] = "placeholder.jpg"

        
        html = soup.prettify()
        return html[:15000]  # prevent token explosion

    except Exception as e:
        return f"Could not fetch website: {e}"
