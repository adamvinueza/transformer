from unittest.mock import mock_open, patch
from transformer.transform import Transform


class TestTransform:

    @staticmethod
    def pass_through(rdr, wr, *params):
        while True:
            b = rdr.read()
            wr(b)
            if not b:
                break

    @patch('fsspec.implementations.local.LocalFileSystem')
    def test_init(self, local):
        tr = Transform(src_fs=local, dest_fs=local)
        assert(tr is not None)
        assert(local == tr.src_fs)
        assert(local == tr.dest_fs)

    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_call(self, mock_fs_open, mock_write, mock_read):
        mock_write.exists.return_value = False
        mock_read.open = mock_fs_open
        tr = Transform(src_fs=mock_read, dest_fs=mock_write)
        tr('src', 'dest', TestTransform.pass_through, [])
        mock_fs_open.assert_called_once_with('src', 'rb')
        mock_write.open.assert_called_once_with('dest', 'wb')

    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    @patch("builtins.open", new_callable=mock_open)
    def test_copy(self, mock_fs_wopen, mock_fs_ropen, mock_write, mock_read):

        # Mock the writing file system
        mock_write.open = mock_fs_wopen
        mock_writer = mock_fs_wopen.return_value

        # Mock the reading file system
        mock_read.open = mock_fs_ropen
        mock_reader = mock_fs_ropen.return_value

        # mocked source and destination file
        src = 'src'
        dest = 'dest'

        tr = Transform(src_fs=mock_read, dest_fs=mock_write)
        tr.copy(src, dest)

        # reading is binary
        mock_fs_ropen.assert_called_once_with(src, 'rb')
        mock_reader.read.assert_called_once()

        # writing is binary
        mock_write.open.assert_called_once_with(dest, 'wb')
        mock_writer.write.assert_called_once_with('data')
