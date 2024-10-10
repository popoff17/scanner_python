from db.db import SEOData, SitesTable
from urllib.parse import urlparse
import requests

class HelperParser:
    def __init__(self):
        pass  # Здесь можно добавить начальные параметры, если они понадобятся

    @staticmethod
    def is_internal_link(base_url, link):
        return urlparse(link).netloc == urlparse(base_url).netloc

    @staticmethod
    def url_exists(session, url):
        return session.query(SEOData).filter_by(url=url).first() is not None

    @staticmethod
    def checkSite(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            return False
