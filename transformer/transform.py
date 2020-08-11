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
    def __init__(
            self,
            fs: AbstractFileSystem = None,
            ow: bool = False) -> None:
        self.overwrite = ow
        if fs is None:
            # By default, use the local file system.
            self.fs = LocalFileSystem()
        else:
            self.fs = fs


class Transform(_FSWrapper):
    """Passes the specified source file through the specified transformation
    operation (using the specified parameters), writing to the specified
    destination file. If the destination file exists it will be overwritten.

    Callable Args:
        src (str): Source file path or URL.
        dest (str): Destination file path or URL.
        op (Callable[Reader, Writer, VarArg()], Any]): Operation to perform.
        params (List[Any]): Operation parameters.
    """
    def __init__(
            self,
            fs: AbstractFileSystem = None,
            ow: bool = False) -> None:
        super().__init__(fs, ow)

    def __call__(
            self,
            src: str,
            dest: str,
            op: Callable[[OpenFile, Writer, VarArg()], Any],
            params: List[Any]) -> None:
        wr = Writer(dest, self.fs, self.overwrite)
        with self.fs.open(src, 'rb') as rdr:
            return op(rdr, wr, *params)


class BulkTransform(_FSWrapper):
    """Transforms input files into output files via the specified operation,
    using the specified dictionary, whose keys are the input file paths and
    whose values are the output file paths.
    """
    def __init__(self, fs: AbstractFileSystem, ow: bool = False) -> None:
        super().__init__(fs, ow)

    def __call__(
            self,
            src_dest_map: Dict[str, str],
            op: Callable[[OpenFile, Writer, VarArg()], Any],
            params: List[Any]) -> None:
        tr = Transform(self.fs)
        for src, dest in src_dest_map.items():
            tr(src, dest, op, *params)
