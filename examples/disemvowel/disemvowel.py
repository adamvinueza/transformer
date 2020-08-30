def disemvowel(rdr, wr) -> None:
    bufsize = 1024
    while True:
        content = rdr.read(bufsize).decode('utf-8')
        b = bytes()
        for i in range(len(content)):
            if content[i] not in 'aeiouAEIOU':
                b += bytes(content[i], 'utf-8')
        # We need to call the Writer even if there is no data, so
        # it knows to close the output stream.
        wr(b)
        if not content:
            break
