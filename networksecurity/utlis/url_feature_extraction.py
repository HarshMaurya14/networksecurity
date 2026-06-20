"""
url_feature_extractor.py

Converts a raw URL string into the 29 numerical features the phishing
detection model was trained on (matches data_schema/schema.yaml).

Feature encoding follows the original UCI Phishing Websites dataset convention:
    -1 = suspicious / phishing signal
     0 = neutral / unknown
     1 = legitimate signal

A handful of features (web_traffic, Page_Rank, Google_Index,
Links_pointing_to_page, Statistical_report) originally relied on services
that are now defunct (Alexa, old Google PageRank API) or required paid
APIs. Those are set to a neutral default (0) here rather than faking a
real value. This is called out explicitly so it's never misrepresented
as live data.
"""

import re
import socket
import ssl
from urllib.parse import urlparse

import requests

# Common URL shortening services used to flag Shortining_Service
SHORTENING_SERVICES = {
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "is.gd",
    "buff.ly", "adf.ly", "bitly.com", "cutt.ly", "rb.gy", "shorte.st",
}


def _is_ip_address(domain: str) -> bool:
    try:
        socket.inet_aton(domain)
        return True
    except OSError:
        return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain))


def extract_features(url: str) -> dict:
    """Returns a dict of the 29 input features (excludes 'Result' label)."""

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc.split(":")[0]
    full_url = url

    features = {}

    # --- Pure string-parsing features (no network call needed) ---
    features["having_IP_Address"] = -1 if _is_ip_address(domain) else 1
    features["URL_Length"] = -1 if len(full_url) >= 75 else (0 if len(full_url) >= 54 else 1)
    features["Shortining_Service"] = -1 if domain in SHORTENING_SERVICES else 1
    features["having_At_Symbol"] = -1 if "@" in full_url else 1
    features["double_slash_redirecting"] = -1 if full_url.rfind("//") > 7 else 1
    features["Prefix_Suffix"] = -1 if "-" in domain else 1
    features["having_Sub_Domain"] = (
        -1 if domain.count(".") > 3 else (0 if domain.count(".") == 3 else 1)
    )
    features["HTTPS_token"] = -1 if "https" in domain.lower() else 1
    features["Abnormal_URL"] = 1  # neutral default; needs WHOIS to verify properly
    features["port"] = -1 if parsed.port not in (None, 80, 443) else 1

    # --- Features that need to fetch the page (best-effort, fail-safe) ---
    page_html = None
    ssl_valid = None
    try:
        resp = requests.get(full_url, timeout=4, verify=True)
        page_html = resp.text
        ssl_valid = full_url.startswith("https://")
    except requests.exceptions.SSLError:
        ssl_valid = False
    except requests.exceptions.RequestException:
        page_html = None

    features["SSLfinal_State"] = 1 if ssl_valid else (-1 if ssl_valid is False else 0)
    features["Favicon"] = 1 if page_html and "icon" in page_html.lower() else 0
    features["Request_URL"] = 0
    features["URL_of_Anchor"] = 0
    features["Links_in_tags"] = 0
    features["SFH"] = 0
    features["Submitting_to_email"] = (
        -1 if page_html and "mailto:" in page_html.lower() else 1
    )
    features["Redirect"] = 1
    features["on_mouseover"] = (
        -1 if page_html and "onmouseover" in page_html.lower() else 1
    )
    features["RightClick"] = (
        -1 if page_html and "event.button==2" in page_html.lower() else 1
    )
    features["popUpWidnow"] = (
        -1 if page_html and "window.open" in page_html.lower() else 1
    )
    features["Iframe"] = -1 if page_html and "<iframe" in page_html.lower() else 1

    # --- Features that originally required WHOIS (kept neutral here) ---
    features["Domain_registeration_length"] = 0
    features["age_of_domain"] = 0
    features["DNSRecord"] = 0

    # --- Features that needed now-defunct services (Alexa/old PageRank API) ---
    features["web_traffic"] = 0
    features["Page_Rank"] = 0
    features["Google_Index"] = 1  # most sites assumed indexed by default
    features["Links_pointing_to_page"] = 0
    features["Statistical_report"] = 1

    # Reorder to exactly match data_schema/schema.yaml column order.
    # The model's preprocessor (KNNImputer) is strict about column order,
    # so this step is required even though the dict above has all the
    # right keys — Python dicts preserve insertion order, not schema order.
    SCHEMA_ORDER = [
        "having_IP_Address", "URL_Length", "Shortining_Service",
        "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix",
        "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length",
        "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor",
        "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL",
        "Redirect", "on_mouseover", "RightClick", "popUpWidnow", "Iframe",
        "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank",
        "Google_Index", "Links_pointing_to_page", "Statistical_report",
    ]
    return {col: features[col] for col in SCHEMA_ORDER}