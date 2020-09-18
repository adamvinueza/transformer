from configparser import ConfigParser
from s3fs import S3FileSystem
from fsspec.implementations.local import LocalFileSystem
from fsspec.implementations.sftp import SFTPFileSystem
import os.path


def S3FS(profile_name):
    creds_path = os.path.join(
        os.path.expanduser('~'),
        '.aws/credentials'
    )
    conf = ConfigParser()
    conf.read(creds_path)
    aws_access_key_id = conf.get(profile, 'aws_access_key_id'),
    aws_secret_access_key = conf.get(profile, 'aws_secret_access_key'),
    aws_session_token = conf.get(profile, 'aws_session_token')
    return s3fs.S3FileSystem(
        anon=False,
        key=aws_access_key_id,
        secret=aws_secret_access_key,
        token=aws_session_token
    )


def LocalFS():
    return LocalFileSystem()


def SFTPFS(host, temppath, username, password, port):
    return SFTPFileSystem(host,
                          temppath,
                          {
                              'username': username,
                              'password': password,
                              'port': port
                          })
