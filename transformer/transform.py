from fsspec import AbstractFileSystem  # type: ignore
from fsspec.implementations.local import LocalFileSystem  # type: ignore
from typing import Any, Callable, Dict
from transformer.io import Writer


class _FSWrapper():
    """A wrapper for AbstractFileSystem implementations that sets the
    LocalFileSystem implementation if None is passed in.
    """
    def __init__(self, fs: AbstractFileSystem) -> None:
        if fs is None:
            # By default, use the local file system.
            self.fs = LocalFileSystem()
        else:
            self.fs = fs


class Transform(_FSWrapper):
    """Creates a reader from src and a Writer that performs the operation on the
    buffered data (using the operation's parameters) and streams the result via
    the Writer to the file at dest.

    Example:
        # filters out all the vowels in a text file, writes output to utf-8.
        def disemvowel(rdr, wr):
            bufsize = 1024
            while True:
                content = str(rdr.read(bufsize)).lower()
                if not content:
                    break
                b = bytes()
                for c in content:
                    if c not in 'aeiou':
                        b += bytes(c, 'utf-8')
                wr(b)

        tr = Transform()
        src = "path/to/source/file"
        dest = "path/to/dest/file"
        tr(src, dest, disemvowel)

    Callable Args:
        src (str): Source file path or URL.
        dest (str): Destination file path or URL.
        op (Callable[Reader, Writer, Any], Any]): Operation to perform.
        params (List[Any]): Operation parameters.
    """
    def __init__(self, fs: AbstractFileSystem = None) -> None:
        super(fs)

    def __call__(
            self,
            src: str,
            dest: str,
            op: Callable[[str, Writer, Any], Any],
            params: Any) -> None:
        wr = Writer(dest, self.fs)
        with self.fs.open(src, 'rb') as rdr:
            return op(rdr, wr, *params)


class BulkTransform(_FSWrapper):
    def __init__(self, fs: AbstractFileSystem) -> None:
        super(fs)

    def __call__(
            self,
            src_dest_map: Dict[str, str],
            op: Callable[[str, Writer, Any], Any],
            params: Any) -> None:
        """Performs the specified operation on each file given as the key in the
        map, and writes the results to the file that is the value in the map.
        """
        tr = Transform(self.fs)
        for src, dest in src_dest_map.items():
            tr(src, dest, op, *params)
