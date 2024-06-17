from htpy import Element, button, div, i, input, p, span


def login_form() -> Element:
  return div[div(".field")[p(".control.has-icons-left.has-icons-right")[
      input(".input", type="email", placeholder="Email"),
      span(".icon.is-small.is-left")[i(".fas.fa-envelope")],
      span(".icon.is-small.is-right")[i(".fas.fa-check")]]],
             div(".field")[p(".control.has-icons-left")[
                 input(".input", type="password", placeholder="Password"),
                 span(".icon.is-small.is-left")[i(".fas.fa-lock")]]],
             div(".field")[p(".control")[button(".button.is-success"
                                                )["""      Login    """]]]]
