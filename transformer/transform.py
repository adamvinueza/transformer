from fsspec import AbstractFileSystem  # type: ignore
from fsspec.core import OpenFile  # type: ignore
from fsspec.implementations.local import LocalFileSystem  # type: ignore
from typing import Any, Callable, Dict, List
from mypy_extensions import VarArg
from transformer.io import Writer


class _FSWrapper(object):
    """A wrapper for AbstractFileSystem implementations that sets the
    LocalFileSystem implementation if None is passed in.
    """
    def __init__(self, fs: AbstractFileSystem = None) -> None:
        if fs is None:
            # By default, use the local file system.
            self.fs = LocalFileSystem()
        else:
            self.fs = fs


class Transform(_FSWrapper):
    """Creates a reader from src and a Writer that performs the operation on the
    buffered data (using the operation's parameters) and streams the result via
    the Writer to the file at dest.

    Callable Args:
        src (str): Source file path or URL.
        dest (str): Destination file path or URL.
        op (Callable[Reader, Writer, Any], Any]): Operation to perform.
        params (List[Any]): Operation parameters.
    """
    def __init__(self, fs: AbstractFileSystem = None) -> None:
        super().__init__(fs)

    def __call__(
            self,
            src: str,
            dest: str,
            op: Callable[[OpenFile, Writer, VarArg()], Any],
            params: List[Any]) -> None:
        wr = Writer(dest, self.fs)
        with self.fs.open(src, 'rb') as rdr:
            return op(rdr, wr, *params)


class BulkTransform(_FSWrapper):
    def __init__(self, fs: AbstractFileSystem) -> None:
        super().__init__(fs)

    def __call__(
            self,
            src_dest_map: Dict[str, str],
            op: Callable[[str, Writer, VarArg()], Any],
            params: List[Any]) -> None:
        """Performs the specified operation on each file given as the key in the
        map, and writes the results to the file that is the value in the map.
        """
        tr = Transform(self.fs)
        for src, dest in src_dest_map.items():
            tr(src, dest, op, *params)
