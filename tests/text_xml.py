from tagic.xml import XML


def test_empty():
    expect = "<root />"
    assert expect == XML("root").render()


def test_empty_root():
    expect = "<?xml version='1.0' encoding='UTF-8' ?>\n<root />"
    assert expect == XML("root", is_root=True).render()


def test_some_content():
    expect = '<root a="bar" b>Fooo</root>'
    assert expect == str(XML("root", attrs={"a": "bar", "b": True})["Fooo"])


def test_some_content_child():
    expect = '<root a="bar" b><child>Baz</child>Fooo</root>'
    child = XML("child")["Baz"]
    assert expect == str(
        XML("root", attrs={"a": "bar", "b": True}, children=[child, "Fooo"])
    )
    assert expect == str(XML("root", attrs={"a": "bar", "b": True})[child, "Fooo"])


def test_some_content_child_indent():
    expect = '<root a="bar" b>\n  <child>\n    Baz\n  </child>\n  Fooo\n</root>\n'
    child = XML("child")["Baz"]
    assert expect == (
        XML("root", attrs={"a": "bar", "b": True}, children=[child, "Fooo"])
    ).render(indent=True)
    assert expect == (XML("root", attrs={"a": "bar", "b": True})[child, "Fooo"]).render(
        indent=True
    )
