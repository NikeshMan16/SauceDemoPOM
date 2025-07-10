import os
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Base URLs
    CENTRAL_BASE_URL = os.getenv("BASE_URL")
    

    # Credentials
    CENTRAL_USERNAME = os.getenv("CENTRAL_USERNAME")
    CENTRAL_PASSWORD = os.getenv("CENTRAL_PASSWORD")
    INSTITUTION_USERNAME = os.getenv("INSTITUTION_USERNAME")
    INSTITUTION_PASSWORD = os.getenv("INSTITUTION_PASSWORD")

    # Central URLs
    CENTRAL_LOGIN_PAGE_URL = CENTRAL_BASE_URL
    ADD_INSTITUTION_USER_URL = urljoin(CENTRAL_BASE_URL + "/", "users_institution/add")
    ADD_BOD_URL = urljoin(CENTRAL_BASE_URL + "/", "bod/add")
    BOD_MANAGEMENT_PAGE = urljoin(CENTRAL_BASE_URL + "/", "bod")

    # Institution URLs
    INSTITUTION_LOGIN_PAGE_URL = INSTITUTION_BASE_URL
    INSTITUTION_DASHBOARD_URL = urljoin(INSTITUTION_BASE_URL + "/", "analytical_dashboard")
    INSTITUTION_USER_MANAGEMENT_URL = urljoin(INSTITUTION_BASE_URL + "/", "users_institution")
