import pytest

from tagic import base, html
from tagic.html import (
    a,
    body,
    br,
    div,
    footer,
    h1,
    head,
    header,
    main,
    meta,
    p,
    script,
    span,
    title,
)
from tagic.html import (
    html as html_tag,
)


def test_html():
    expect = "<!DOCTYPE html>\n<html />"
    assert expect == html_tag().render()


def test_str():
    expect = "<!DOCTYPE html>\n<html />"
    assert expect == str(html_tag())


def test_repr():
    expect = "<!DOCTYPE html>\n<html />"
    assert expect == repr(html_tag())


def test_html_with_content():
    base.DOMConfig.FULL_XHTML = False
    try:
        expect = (
            "<!DOCTYPE html>\n"
            "<html><head><title>Fooo</title></head><body><main>xxx</main></body></html>"
        )
        assert expect == html.html[head[title["Fooo"]], body[main["xxx"]]].render()

        base.DOMConfig.FULL_XHTML = True

        expect = (
            '<?xml version="1.0" encoding="UTF-8" ?>\n'
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
            '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
            "<html><head><title>Fooo</title></head><body><main>xxx</main></body></html>"
        )
        assert expect == html.html[head[title["Fooo"]], body[main["xxx"]]].render()
    finally:
        base.DOMConfig.FULL_XHTML = False


def test_a_empty_str():
    expect = '<a id="foo" href="https://example.com"></a>'
    assert expect == a(href="https://example.com", id="foo")[""].render()


def test_a_no_content():
    expect = '<a id="foo" href="https://example.com" />'
    assert expect == a(href="https://example.com", id="foo").render()


def test_basic_tags():
    expect = '<div id="foo" title="bar">XYZ</div>'
    assert expect == div(title="bar", id="foo")["XYZ"].render()


def test_adding_classes():
    tag = div(class_="foo foo")["XYZ"]
    assert '<div class="foo foo">XYZ</div>' == tag.render()

    tag.add_class("foo", "foo")
    assert '<div class="foo">XYZ</div>' == tag.render()

    tag.add_class("bar")
    assert '<div class="foo bar">XYZ</div>' == tag.render()

    tag.add_class("foo", "bar")
    assert '<div class="foo bar">XYZ</div>' == tag.render()

    tag.add_class("bar")
    assert '<div class="foo bar">XYZ</div>' == tag.render()

    tag.add_class("foo", "baz", "bar")
    assert '<div class="foo bar baz">XYZ</div>' == tag.render()


def test_removing_classes():
    tag = div()
    assert "<div />" == tag.render()

    tag.remove_class("foo", "bar", "baz")
    assert "<div />" == tag.render()

    tag.add_class("foo", "bar", "baz")
    assert '<div class="foo bar baz" />' == tag.render()

    tag.remove_class("foo", "foo", "baz")
    assert '<div class="bar" />' == tag.render()

    tag.remove_class("bar", "baz")
    assert "<div />" == tag.render()


def test_can_add_to_children():
    expect = '<div id="foo" title="bar">XYZ</div>'
    assert expect == div(title="bar", id="foo", children=["XYZ"]).render()


def test_error_on_multiple_contents():
    # test on all html tags
    md = html.__dict__
    for c in md:
        if (
            isinstance(md[c], type)
            and md[c].__module__ == html.__name__
            and md[c].__name__ == md[c].__name__.lower()
        ):
            with pytest.raises(TypeError):
                md[c]("XYZ")  # allways need args
                raise ValueError(c)


def test_data_attr():
    expect = (
        '<div id="foo" title="bar" something-else="bar" data-hx-swap="on" '
        'aria-autocomplete="on" aria-checked>XYZ</div>'
    )
    assert (
        expect
        == div(
            title="bar",
            id="foo",
            data_attr={"hx-swap": "on"},
            aria_attr={"autocomplete": "on", "checked": True},
            attr={"something-else": "bar"},
        )["XYZ"].render()
    )


def test_add_html_content():
    # text added to a node will be escaped
    assert "<div>&lt;p&gt;XY&amp;Z&lt;/p&gt;</div>" == div["<p>XY&Z</p>"].render()
    # use NoEscape to add unescaped html / xml / text
    assert (
        "<div><p>XY&amp;Z</p></div>" == div[base.NoEscape("<p>XY&amp;Z</p>")].render()
    )


def test_bool_attr():
    base.DOMConfig.FULL_XHTML = False
    try:
        assert "<div autofocus foo-bar />" == str(
            div(autofocus=True, attr={"foo-bar": True, "bar-foo": False})
        )
        base.DOMConfig.FULL_XHTML = True
        assert '<div autofocus="autofocus" foo-bar="foo-bar" />' == str(
            div(autofocus=True, attr={"foo-bar": True, "bar-foo": False})
        )
    finally:
        base.DOMConfig.FULL_XHTML = False


def test_indent():
    base.DOMConfig.INDENT = 2
    try:
        expect = (
            "<div>\n"
            "  <p>\n"
            "    here we have some text\n"
            "    <br />\n"
            "    and some more text\n"
            "    <span>\n"
            "      This is special text\n"
            "    </span>\n"
            "  </p>\n"
            '  <p id="foo">\n'
            "    some more text\n"
            "  </p>\n"
            "</div>\n"
        )
        assert expect == div[
            p[
                "here we have some text",
                br(),
                "and some more text",
                span["This is special text"],
            ],
            p(id="foo")["some more text"],
        ].render(indent=True)

        # you can change the indent per level with the config
        base.DOMConfig.INDENT = 4
        expect = (
            "<div>\n"
            "    <p>\n"
            "        here we have some text\n"
            "        <br />\n"
            "        and some more text\n"
            "        <span>\n"
            "            This is special text\n"
            "        </span>\n"
            "    </p>\n"
            "</div>\n"
        )
        assert expect == div[
            p[
                "here we have some text",
                br(),
                "and some more text",
                span["This is special text"],
            ]
        ].render(indent=True)
    finally:
        base.DOMConfig.INDENT = 2


def test_readme():
    assert (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "  <head>\n"
        "    <title>\n"
        "      Example Website\n"
        "    </title>\n"
        '    <meta content="This is an example website build with tagic" '
        'name="description" />\n'
        '    <meta charset="utf-8" />\n'
        "  </head>\n"
        "  <body>\n"
        '    <header id="header">\n'
        "      <h1>\n"
        "        Awesome\n"
        "      </h1>\n"
        "    </header>\n"
        "    <main>\n"
        "      <p>\n"
        "        Some text \n"
        "        <span>\n"
        "          with tags\n"
        "        </span>\n"
        "        in between\n"
        "      </p>\n"
        "    </main>\n"
        "    <footer hidden />\n"
        "  </body>\n"
        "</html>\n"
        ""
    ) == html_tag[
        head[
            title["Example Website"],
            meta(
                name="description",
                content="This is an example website build with tagic",
            ),
            meta(
                charset="utf-8",
            ),
        ],
        body[
            header(id="header")[h1["Awesome"]],
            main[p["Some text ", span["with tags"], "in between"]],
            footer(hidden=True),
        ],
    ].render(
        indent=True
    )


def test_script_is_special():
    assert '<script src="/static/htmx.min.js" type="text/javascript"></script>' == str(
        script(type="text/javascript", src="/static/htmx.min.js")
    )
    assert "<script type=\"text/javascript\">console.log('test');</script>" == str(
        script(type="text/javascript")[base.NoEscape("console.log('test');")]
    )
