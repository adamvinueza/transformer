def disemvowel(rdr, wr) -> None:
    bufsize = 1024
    while True:
        content = rdr.read(bufsize).decode('utf-8')
        if not content:
            break
        b = bytes()
        for i in range(len(content)):
            if content[i] not in 'aeiouAEIOU':
                b += bytes(content[i], 'utf-8')
        wr(b)

