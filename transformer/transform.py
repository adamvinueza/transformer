from fsspec import AbstractFileSystem  # type: ignore
from fsspec.core import OpenFile  # type: ignore
from fsspec.implementations.local import LocalFileSystem  # type: ignore
from typing import Any, Callable, Dict, List
from mypy_extensions import VarArg
from transformer.io import Writer


class _FSWrapper(object):
    """A wrapper for AbstractFileSystem implementations that sets the
    LocalFileSystem implementation if None is passed in.

    Args:
        src_fs (AbstractFileSystem): The source file system.
        dest_fs (AbstractFileSystem): The destination file system.
        overwrite (bool) = False: If the destination file exists, overwrite it.
    """
    src_fs: AbstractFileSystem
    dest_fs: AbstractFileSystem
    overwrite: bool

    def __init__(
            self,
            src_fs: AbstractFileSystem = None,
            dest_fs: AbstractFileSystem = None,
            overwrite: bool = False) -> None:
        self.overwrite = overwrite
        if src_fs is None and dest_fs is None:
            src_fs = dest_fs = LocalFileSystem()
        elif bool(src_fs is None) != bool(dest_fs is None):
            if src_fs is None:
                raise ValueError("src_fs is empty")
            if dest_fs is None:
                raise ValueError("dest_fs is empty")
        self.src_fs = src_fs
        self.dest_fs = dest_fs


class Transform(_FSWrapper):
    """Reads a file, runs it through a transformation, and writes the result to
    a destination.

    Args:
        src_fs (AbstractFileSystem): The source file system.
        dest_fs (AbstractFileSystem): The destination file system.
        overwrite (bool) = False: If the destination file exists, overwrite it.

    Callable Args:
        src (str): Source file path or URL.
        dest (str): Destination file path or URL.
        op (Callable[OpenFile, Writer, VarArg()], Any]): Operation to perform.
        params (List[Any]): Operation parameters.
    """
    def __init__(
            self,
            src_fs: AbstractFileSystem = None,
            dest_fs: AbstractFileSystem = None,
            overwrite: bool = False) -> None:
        super().__init__(src_fs, dest_fs, overwrite)

    def __call__(
            self,
            src: str,
            dest: str,
            op: Callable[[OpenFile, Writer, VarArg()], Any],
            params: List[Any]) -> Any:
        wr = Writer(dest, self.dest_fs, self.overwrite)
        with self.src_fs.open(src, 'rb') as rdr:
            return op(rdr, wr, *params)

    def copy(self, src: str, dest: str, bufsize: int = -1) -> None:
        """Copies src to dest.
        Both src and dest paths must be valid in the respective file systems.
        """
        with self.src_fs.open(src, 'rb', bufsize) as rdr:
            with self.dest_fs.open(dest, 'wb', bufsize) as wr:
                wr.write(rdr.read())

    def fcopy(self, 
              src: str,
              dest: str,
              fltr: Callable,
              bufsize: int = -1,
              **kwargs) -> None:
        """Copies src to dest, passing read bytes through a filter.

        The filter takes a sequence of bytes and whatever keyword arguments are
        passed in, and returns a sequence of bytes.

        Both src and dest paths must be valid in the respective file systems.
        """
        with self.src_fs.open(src, 'rb', bufsize) as rdr:
            with self.dest_fs.open(dest, 'wb', bufsize) as wr:
                while True:
                    b = rdr.read(bufsize)
                    if not b:
                        wr.flush()
                        break
                    wr.write(fltr(b, **kwargs))


class BulkTransform(_FSWrapper):
    """Transforms input files into output files via the specified operation,
    using the specified dictionary, whose keys are the input file paths and
    whose values are the output file paths.

    Args:
        src_fs (AbstractFileSystem): The source file system.
        dest_fs (AbstractFileSystem): The destination file system.
        overwrite (bool) = False: If the destination file exists, overwrite it.

    Callable Args:
        src_dest_map (dict): Mapping of source files to destination files.
        op (Callable[OpenFile, Writer, VarArg()], Any]): Operation to perform.
        params (List[Any]): Operation parameters.
    """
    def __init__(
            self,
            src_fs: AbstractFileSystem = None,
            dest_fs: AbstractFileSystem = None,
            overwrite: bool = False) -> None:
        super().__init__(src_fs, dest_fs, overwrite)

    def __call__(
            self,
            src_dest_map: Dict[str, str],
            op: Callable[[OpenFile, Writer, VarArg()], Any],
            params: List[Any]) -> Any:
        tr = Transform(src_fs=self.src_fs,
                       dest_fs=self.dest_fs,
                       overwrite=self.overwrite)
        for src, dest in src_dest_map.items():
            return tr(src, dest, op, *params)
