from dataclasses import dataclass, field, fields
from html import escape
from typing import ClassVar, Iterable, Protocol, Self


class CanRender(Protocol):
    def do_render(self, indent: str | None) -> str:  # pragma: no cover
        ...


class DOMConfig:
    # Specify the indent on rendering for every level.
    INDENT = 2
    # Render the document xhtml1 complient. See
    # https://de.wikipedia.org/wiki/Extensible_Hypertext_Markup_Language
    FULL_XHTML = False


class _Meta(type):
    """Allow []-access on the class of Nodes."""

    def __getitem__(self, child: str | CanRender | Iterable[str | CanRender]) -> "Node":
        return self()[child]  # type: ignore


@dataclass(kw_only=True, slots=True)
class Node(metaclass=_Meta):
    NAME: ClassVar[str | None] = None
    attr: dict[str, str | bool] = field(default_factory=dict)
    children: list[str | CanRender] = field(default_factory=list)

    def __getitem__(self, child: str | CanRender | Iterable[str | CanRender]) -> Self:
        """Add children to the node via []-syntax."""
        if isinstance(child, Iterable) and not isinstance(child, str):
            self.children = list(child)
        else:
            self.children = [child]

        return self

    @property
    def tag_name(self) -> str:
        return self.NAME or self.__class__.__name__

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return self.render()

    def render(self, indent: bool = False) -> str:
        if indent:
            return self.do_render("")
        else:
            return self.do_render(None)

    def do_render(self, indent: str | None) -> str:
        indent_str = ""
        new_indent = None
        if indent is not None:
            new_indent = indent + (" " * DOMConfig.INDENT)
            indent_str = indent
        result = f"{indent_str}<{self.tag_name}"
        no_content = len(self.children) == 0

        def indent_newline() -> None:
            nonlocal result
            if indent is not None:
                result += "\n"

        result += self._render_attr()

        if no_content:
            result += " />"
        else:
            result += ">"
        indent_newline()

        result += self._render_content(new_indent)

        if not no_content:
            result += f"{indent_str}</{self.tag_name}>"
            indent_newline()

        return result

    def _render_content(self, indent: str | None) -> str:
        result = ""

        for child in self.children:
            if isinstance(child, str):
                result += f"{indent or ''}{escape(child)}"
                if indent is not None:
                    result += "\n"
            else:
                result += child.do_render(indent)
        return result

    def _render_attr(self) -> str:
        result = ""
        for field_ in fields(self):
            if field_.name in (
                "tag_name",
                "children",
                "aria_attr",
                "data_attr",
                "attr",
            ):
                continue
            value = getattr(self, field_.name)
            if value is not None and value is not False:
                name = field_.name
                if name.endswith("_"):
                    # e.g. class_ -> class
                    name = name[:-1]
                # e.g. accept_charset -> accept-charset
                name = name.replace("_", "-")
                result += self._render_single_attr(name, value)

        for name, value in self.attr.items():
            result += self._render_single_attr(name, value)

        return result

    def _render_single_attr(self, name: str, value: str | bool) -> str:
        if isinstance(value, bool):
            if value is True:
                if DOMConfig.FULL_XHTML:
                    return f' {name}="{name}"'
                else:
                    return f" {name}"
            # False will be ignored
            return ""
        else:
            return f' {name}="{value}"'


@dataclass
class NoEscape(CanRender):
    """Add string content, that should not be html escaped."""

    content: str

    def do_render(self, indent: str | None) -> str:
        return self.content
