[![CI](https://github.com/tammoippen/tagic/actions/workflows/CI.yml/badge.svg)](https://github.com/tammoippen/tagic/actions/workflows/CI.yml)
[![PyPi version](https://img.shields.io/pypi/v/tagic.svg)](https://pypi.python.org/pypi/tagic)
[![Python Versions](https://img.shields.io/badge/python-3.11-brightgreen.svg)](https://img.shields.io/badge/python-3.11-brightgreen.svg)
[![Downloads](https://static.pepy.tech/badge/tagic/month)](https://pepy.tech/project/tagic)
[![codestyle black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
# tagic

Build html / xhtml with a nice syntax.

## Goals

- generate html / xhtml with a nice syntax
- have typing support
- have editor support for arguments, I used MDN as a reference.
- KISS: no more than generation

## Install

```sh
> pip install tagic
```

## Example

```py
from tagic.html import *

print(
    html[
      head[
          title["Example Website"],
          meta(
              name="description",
              content="This is an example website build with tagic",
          ),
      ],
      body[
          header(id="header")[h1["Awesome"]],
          main[p["Some text ", span["with tags"], "in between"]],
          footer(hidden=True),
      ],
  ].render(indent=True)
)
```

Will return

```html
<!DOCTYPE html>
<html>
  <head>
    <title>
      Example Website
    </title>
    <meta content="This is an example website build with tagic" name="description" />
  </head>
  <body>
    <header id="header">
      <h1>
        Awesome
      </h1>
    </header>
    <main>
      <p>
        Some text
        <span>
          with tags
        </span>
        in between
      </p>
    </main>
    <footer hidden>

    </footer>
  </body>
</html>
```

## Similar Projects

- [dominate](https://github.com/Knio/dominate): missing the typing support and editor support for arguments
- [domonic](https://github.com/byteface/domonic): to broad of a scope, with parsing, js and style and queries.
- [domini](https://gitlab.com/deepadmax/domini): missing editor support for arguments
- [htmler](https://github.com/ashep/htmler): missing the typing support and editor support for arguments
- [PyHTML](https://github.com/cenkalti/pyhtml): missing the typing support and editor support for arguments
- [pyhtmlgen](https://github.com/danvran/pyhtmlgen): incomplete
- [html](https://pypi.org/project/html/): i do not like syntax and missing the typing support and editor support for arguments
- [MarkupPy](https://github.com/tylerbakke/MarkupPy)
- [yattag](https://www.yattag.org/): i do not like syntax
- [py-microhtml](https://github.com/elonen/py_microhtml): funny tag names and no editor support for arguments
- [py3html](https://github.com/ozcanyarimdunya/py3html): no editor support for arguments
- [fast-html](https://github.com/pcarbonn/fast_html)
- [py2html](https://github.com/am230/py2html) not in pypi, but i like the syntax and took inspiration
