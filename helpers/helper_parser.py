from db.db import SEOData, SitesTable
from urllib.parse import urlparse

class HelperParser:
    def __init__(self):
        pass  # Здесь можно добавить начальные параметры, если они понадобятся

    @staticmethod
    def is_internal_link(base_url, link):
        return urlparse(link).netloc == urlparse(base_url).netloc

    @staticmethod
    def url_exists(session, url):
        return session.query(SEOData).filter_by(url=url).first() is not None
