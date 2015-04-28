# net-diff
Compare two large files over a network without transferring a buncha data

### Usage
net-diff requires one person to be the host (which will require their computer/router to have appropriate firewall rules that allow communication on the specified port)

Server: ```python netdiff.py file [port]```

Client: ```python netdiff.py file host [port]```

After the connection is established, net-diff will perform the following steps to find the earliest byte where the files diverge between machines:

1. split the file data in half
2. compute the md5 sums of the first and second halves
3. communicate md5 sums to peer
4. check if md5 sums of either half differ
5. for the pair of halves that differ (or if both sets differ, the first half) split it in half and jump back to step 2
6. keep doing this until the size of the data to be split is 1 byte
7. report the offset of that byte

### Limitations
Currently net-diff is only capable of reporting the very first byte that differs between two files, and only on files of the same size. It also has to load the entire file into RAM.

### Future Work
- Function on files of different file sizes
- Reporting all bytes that differ (including when "streaks" of bytes differ)
- If the bytes are sufficiently small, and are text, display them (much like [diff](http://unixhelp.ed.ac.uk/CGI/man-cgi?diff) does)
- Ease up RAM usage by using numpy arrays (to prevent copying data with each recurse)

### Example
Alice has a large 2GB file that she sent to Bob. When the file arrived, however, one or two bytes somewhere in it got corrupted. The rest of the bytes were intact. Alice and Bob need a way to figure out the offset to where the differing bytes are without having to re-transfer all of the data. Then Bob can fix his copy of the file with a hex editor or patch. The file is named top_secret.rar. Alice's IP is 28.57.203.49.

Alice runs the following on her computer:
```
python netdiff.py 8000
```

And Bob runs the following on his computer:
```
python netdiff.py 28.57.203.49 8000
```

Bob's program would then report the following output:
```
Loaded top_secret.rar (2000000000 bytes) into memory!
Hash: 9a81c422f886061462b1e65032e37b1b

Trying to connect to 28.57.203.49 on port 8000...
Connected to 28.57.203.49!

These files start to differ at offset 0x3B9FFA20
```
