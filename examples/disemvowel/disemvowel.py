def disemvowel(rdr, wr) -> None:
    bufsize = 1024
    while True:
        content = rdr.read(bufsize).decode('utf-8')
        content_lc = content.lower()
        if not content:
            break
        b = bytes()
        for i in range(len(content)):
            if content_lc[i] not in 'aeiou':
                b += bytes(content[i], 'utf-8')
        wr(b)

