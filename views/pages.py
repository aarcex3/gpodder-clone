from htpy import Element, h1, div
from .components import login_form

def home_page() -> Element:
  return h1('.title.is-1')["Home"]


def login_page() -> Element:
  return div[h1('.title.is-1')["Login"],login_form]
