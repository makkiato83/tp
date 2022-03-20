# tp  - Tor Pipe

A small script (just one .py file) to _pipe_ over tor. It uses the Python standard library and the `stem` package. 

## Installation
```
git clone https://github.com/makkiato83/tp
cd tp
pip install --editable .
```

## Description

`tp` gets as input the `stdin` and does the following:
1) connects to the Tor SOCKS proxy (use the `--port` modifier to provide the port, default is 9151 which is used by the Tor Browser), 
2) forks into a Hidden HTTP server on the fly and terminates. 
    - using option (`-b`/`--background`) `tp` does not fork and terminates together with the HTTP server. This could be useful to know when/if somebody got the content.

The spawned hidden HTTP service runs in the background until it receives a `GET` requests. It then delivers the input (`stdin`) and terminates.
This means that the data is delivered to at most one recipient.

**Option -b/--blocking**: alternatively, with the flag `--blocking` or `-b`, `tp` returns only when the content is delivered.

### Example 1:
Assume Alice and Bob are in separate networks.\
Alice can share a document with Bob as follows:
```
alice:~ cat README.md | tp`
ndefqjsjly6h7a4ysra25jhubo7eipqfyb43fmvjxkuxixp4vnxixeyd.onion
```

Then Alice communicates by some mean the onion address to Bob.\
Bob can then receive as follows:

```
bob:~ torsocks curl ndefqjsjly6h7a4ysra25jhubo7eipqfyb43fmvjxkuxixp4vnxixeyd.onion >> received.txt
```
The communication is fully encrypted by the TOR onion protocol.\
Note, however, that Alice does not know if it was Bob or somebody else to receive the file!

### Example 2:

Alice wants to share her mail with Bob in a private way. She also wants to see when the message is delivered.

```commandline
alice:~ echo "Hi bob, write to me at myemail@example.com" | tp -b
mpdiziullb63u3577kpnucm5lojaivfifkaxxvzqrqot3pgfdb3ijoqd.onion
```

```commandline
bob:~ torsocks curl mpdiziullb63u3577kpnucm5lojaivfifkaxxvzqrqot3pgfdb3ijoqd.onion
Plese write to me at myemail@example.com
```

### Example 3:

In Alice's machine, TOR is listening on port 7000.\
Alice wants to send a gpg signed message to Bob in a private way.

```commandline
alice:~ gpg --clearsign | tp
5uvzimj5263mnua5glux5qryzpgndidoz6shvrzwxn22gmz4qhzzlnqd.onion
```

Bob opens the onion address with the Tor browser and sees:

```commandline
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

Hi bob! This is a message from me, Alice :)
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCAAdFiEEkQgDD8OI7C+4e0Mz3pfEO2irY0oFAmI3VKsACgkQ3pfEO2ir
Y0oItw//f6xvdvirzpfLett0s9wC3bm7mZGt0W3IyKzIQoLd1Fr/oJjJxfoCiUVG
EKsgsQuS1kVlvnjlkdK392UBsnBqT46kYHRqtu+yqE44Z7kdf+U0Jgr6IIxw0A6b
pApIpaba4uL/GNhCxYYs9ZxpMAOa20NhN5b8OoVicpbJjqiZJ+/6yfJ3h1ZP+Bcd
VD08mYM8aB5G1aN1m/FNSLdHd4lQARo/E2ie24yI3aj+EO2fLOEjyufXrhS21PPC
Riu7XcGuuC6oSUsiP2QJouo9lFV44Y1iICx3+vVsH83PjbP+IEs3OyPllGYBlce+
85Bimnqvxqyjfg1V1jS0tSsyJ5UjI9N5cNlBgyXZS1OOLPLfFKWzAVPHVMFIaHjl
r7XXKrlQ1g4g9Drbli932/c8CuNcu+g8CRHa3gzAJ8+Y4qSIXJTBDUP1RofHomRp
Lp563Ap/Ctn4OBR5kBkzcbZ3fKDpZsAF2NMIJEmugAQpR4oVT2pvc6716R5mgYrf
smbHKaAldgU7fRMln1nn/JW/7/aNg61HOSHcBP9XtQnGc62y9bEGo+m1Yj28XrVM
UuIJXDO6XwEobUzL0zto/aPm/HO+T6otxbHi574pub/c+U8iSfistfBUriiEnhuK
LjWf1ugsp27cxJ7H2rj1sk14DSxAQE+pEPFFrpdmTktOSzzPXzI=
=ylu9
-----END PGP SIGNATURE-----
```

