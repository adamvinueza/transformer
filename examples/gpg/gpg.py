import gnupg

def encrypt(rdr, wr, home, passphrase):
    gpg = gnupg.GPG(gnupghome=home)
    gpg.on_data = wr
    status = gpg.encrypt_file(rdr, passphrase=passphrase, encrypt=False)
    if not status.ok:
        raise ValueError(f"encryption failed: status={status.status}, "
                         f"error={status.stderr}")


def decrypt(rdr, wr, home, passphrase):
    gpg = gnupg.GPG(gnupghome=home)
    gpg.on_data = wr
    status = gpg.decrypt_file(rdr, passphrase=passphrase)
    if not status.ok:
        raise ValueError(f"decryption failed: status={status.status}, "
                         f"error={status.stderr}")
