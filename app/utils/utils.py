import hashlib
import json
import re
import xml.etree.ElementTree as ET
from typing import List

from fastapi.exceptions import HTTPException

from app.schemas.schemas import Podcast


def get_file_hash(podcasts: List[Podcast]) -> str:
    """
    Generate a hash for a list of podcasts.
    """
    if not podcasts:
        return ""
    try:
        podcasts_json = json.dumps(
            [podcast.model_dump_json() for podcast in podcasts], sort_keys=True
        )
        hash_object = hashlib.sha256(podcasts_json.encode())
        return hash_object.hexdigest()

    except Exception as e:
        print(f"Error generating hash: {e}")
        return ""


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_secure_password(password: str) -> bool:
    min_length = 8
    pattern_uppercase = r"[A-Z]"
    pattern_lowercase = r"[a-z]"
    pattern_digit = r"\d"
    pattern_special = r"[^A-Za-z0-9]"
    if len(password) < min_length:
        return False
    if not re.search(pattern_uppercase, password):
        return False
    if not re.search(pattern_lowercase, password):
        return False
    if not re.search(pattern_digit, password):
        return False
    if not re.search(pattern_special, password):
        return False
    return True


def parse_opml(file_content: bytes) -> List[Podcast]:
    root = ET.fromstring(file_content)
    outlines = root.findall(".//outline")
    podcasts = []
    for outline in outlines:
        title = outline.get("title")
        type_ = outline.get("type")
        xmlUrl = outline.get("xmlUrl")
        htmlUrl = outline.get("htmlUrl")
        podcasts.append(
            Podcast(title=title, type_=type_, xmlUrl=xmlUrl, htmlUrl=htmlUrl)
        )
    return podcasts


def handle_exception(error_message: str, status_code: int):
    raise HTTPException(status_code=status_code, detail=error_message)


"""
from fake_useragent import UserAgent
from fake_useragent.fake import FakeUserAgent
async def get_podcast_lang(xml_url: str, html_url: str) -> str:
    ua: FakeUserAgent = UserAgent()
    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": ua.random}
        try:
            try:
                async with session.get(xml_url, headers=headers) as response:
                    response.raise_for_status()
                    content = await response.read()
                root = ET.fromstring(content)
                language_element = root.find(".//language")
                return (language_element.text if language_element is not None else "No Lang")
            except (ET.ParseError, aiohttp.ClientError):
                pass
            async with session.get(html_url, headers=headers) as response:
                response.raise_for_status()
                content_type = response.headers.get("content-type")
                if content_type is not None and "html" in content_type:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    lang_tag = soup.html.get("lang", None)
                    if lang_tag:
                        return lang_tag
                    else:
                        return "No Lang"
                else:
                    return "Unsupported content type"

        except aiohttp.ClientError as e:
            print(
                f"Error retrieving content from {xml_url} or {html_url}: {e}")
        except Exception as e:
            print(f"Error parsing content from {xml_url} or {html_url}: {e}")
"""
