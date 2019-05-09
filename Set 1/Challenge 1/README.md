This is a simple conversion of hex to base64. This is easily achievable with Python.

Something that may be easily missed: `Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing. `

In order to achieve this:

1. Input = Hex String
2. Convert input to bytes.
3. Convert bytes to base 64.
4. Print result.

Python includes a handy way to convert a hex strin to bytes: `bytes.fromhex()`
It also has a standard library `base64` which includes `base64.b64encode()`
So we simply call these functions in the right order and print the result.

Our function properly prints
`b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'`

The `b` in front of the string means it's a bytes type instead of a string.