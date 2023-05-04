"""
Tracing utils
"""
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union


_Writer = Callable[[str], None]
_Processor = Callable[[Tuple[str, ...], Tuple[Any, ...]], None]


class TagTracer:
    def __init__(self) -> None:
        self._tags2proc: Dict[Tuple[str, ...], _Processor] = {}
        self._writer: Optional[_Writer] = None
        self.indent = 0

    def get(self, name: str) -> "TagTracerSub":
        return TagTracerSub(self, (name,))

    def _format_message(self, tags: Sequence[str], args: Sequence[object]) -> str:
        if isinstance(args[-1], dict):
            extra = args[-1]
            args = args[:-1]
        else:
            extra = {}

        content = " ".join(map(str, args))
        indent = "  " * self.indent

        lines = [f'{indent}{content} [{":".join(tags)}]\n']

        lines.extend(f"{indent}    {name}: {value}\n" for name, value in extra.items())
        return "".join(lines)

    def _processmessage(self, tags: Tuple[str, ...], args: Tuple[object, ...]) -> None:
        if self._writer is not None and args:
            self._writer(self._format_message(tags, args))
        try:
            processor = self._tags2proc[tags]
        except KeyError:
            pass
        else:
            processor(tags, args)

    def setwriter(self, writer: _Writer) -> None:
        self._writer = writer

    def setprocessor(
        self, tags: Union[str, Tuple[str, ...]], processor: _Processor
    ) -> None:
        if isinstance(tags, str):
            tags = tuple(tags.split(":"))
        else:
            assert isinstance(tags, tuple)
        self._tags2proc[tags] = processor


class TagTracerSub:
    def __init__(self, root: TagTracer, tags: Tuple[str, ...]) -> None:
        self.root = root
        self.tags = tags

    def __call__(self, *args: object) -> None:
        self.root._processmessage(self.tags, args)

    def get(self, name: str) -> "TagTracerSub":
        return self.__class__(self.root, self.tags + (name,))
