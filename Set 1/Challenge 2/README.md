Challenge 2:

# Fixed XOR
#### Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:
`1c0111001f010100061a024b53535009181c`

after hex decoding, and when XOR'd against:
`686974207468652062756c6c277320657965`

should produce:
`746865206b696420646f6e277420706c6179`

---

# Walkthrough

This seems simple enough. XOR is a bitwise operation, short for `exclusive or`. It compares the bits of two binary values, and sets the resulting bit to 1 only if the bits compared are not equal. For example:

```
1001011
0001100
```
This will produce: `10001001`

XOR, from what I've read so far, is used in a lot of encryption due to the fact that it's reversible. In other words:
`a ^ b = c` `b ^ c = a`
The little carrot sign is shorthand for XOR, and also the operator which python (as well as many other languages) use.

So all we have to do is:
1. Ensure our input is interpreted as hex.
2. Convert to bytes.
3. Return input1 ^ input2

Step two should happen automatically if python allows bitwise operations on hex values.