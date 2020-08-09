from fsspec import AbstractFileSystem  # type: ignore
from typing import Any


class Writer():
    """Writer streams data to a destination file."""
    def __init__(self, dest: str, fs: AbstractFileSystem) -> None:
        self.fout = fs.open(dest, 'wb')

    def __call__(self, data: Any) -> bool:
        if data:
            self.fout.write(data)
        else:
            self.fout.close()
        return False
