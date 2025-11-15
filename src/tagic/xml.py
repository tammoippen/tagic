from dataclasses import dataclass

from .base import Elements, Node


@dataclass(kw_only=True, slots=True, repr=False)
class XML(Node):
    _name: str | None
    _is_root: bool

    def __init__(
        self,
        name: str | None = None,
        *,
        attrs: dict[str, str | bool] | None = None,
        children: Elements | None = None,
        is_root: bool = False,
    ) -> None:
        if attrs is None:
            attrs = {}
        if children is None:
            children = []
        super(XML, self).__init__(attr=attrs, children=children)
        self._name = name
        self._is_root = is_root

    @property
    def tag_name(self) -> str:
        return self._name or super(XML, self).tag_name

    def do_render(self, indent: str | None) -> str:
        render = ""
        if self._is_root:
            render = "<?xml version='1.0' encoding='UTF-8' ?>\n"
        return render + super(XML, self).do_render(indent)
