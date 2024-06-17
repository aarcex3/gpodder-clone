from htpy import Element, Node, body, head, html, link, meta


def base(page: Node) -> Element:
  return html(lang="en")[
            head[
              meta(charset="UTF-8"),
              meta(name="viewport", content="width=device-width, initial-scale=1.0"),
              link(rel="stylesheet",href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css")
            ],
            body[
              page
            ]
          ]
