# tp  - Tor Pipe

A minimalistic script (just one .py file) to *pipe* over tor. It uses the Python standard library and the the `stem` package. 

## Installation
```
git clone https://github.com/makkiato83/tp
cd tp
pip install --editable .
```

## Description

`tp` connects to the Tor SOCKS proxy (use the `--port` modifier to provide the port, default is 9150 which is used by the Tor Browser), forks into a Hidden HTTP server on the fly and terminates.

The spawned hidden HTTP service runs in the background until it receives a `GET` requests. It then delivers the serves the `stdin` and terminates.


This means that the data is delivered to most to one recipient.

**Option -b/--blocking**: alternatively, with the flag `--blocking` or `-b`, `tp` returns only when the content is delivered.

### Example 1:
Machine1: \
`cat README.md | tp`\
` sdout> ndefqjsjly6h7a4ysra25jhubo7eipqfyb43fmvjxkuxixp4vnxixeyd.onion`

Machine2: \
`torsocks curl ndefqjsjly6h7a4ysra25jhubo7eipqfyb43fmvjxkuxixp4vnxixeyd.onion >> received.txt`


### Example 2:

Machine1: \
`echo "Plese write to me at myemail@example.com" | tp`\
`sdout > mpdiziullb63u3577kpnucm5lojaivfifkaxxvzqrqot3pgfdb3ijoqd.onion`\
Machine 2:\
`torsocks curl mpdiziullb63u3577kpnucm5lojaivfifkaxxvzqrqot3pgfdb3ijoqd.onion`\
`sdout >  Plese write to me at myemail@example.com`

### Example 3:

