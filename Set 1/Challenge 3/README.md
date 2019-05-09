# Challenge 3: Single-byte XOR cipher

The hex encoded string:

`1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
`

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.
Achievement Unlocked

`You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.`

---

# Walkthrough

Ah, now it's getting a bit harder. Doing a XOR on each character in the string against each possible byte value (0 - 255) isn't too complicated. It's the analyzing of the result that's is completely foreign to me.

There's a suggestion about character frequency, but instead of creating my own subpar scoring system for English I'm going to do some research. The comment about the joke at the bottom seems interesting...

After some research I found the following:
`etaoin shrdlu is the approximate order of frequency of the 12 most commonly used letters in the English language`

It became a running joke in old newspapers and Linotype/Intertype machine keyboard were arranged with keys in that order.

So... if I really want to create a basic english scoring system I could count the number of occurences of e, t, a, etc... and then *do some kind of math stuff*...

I know myself enough to understanding my limitations, and this is an area I have a complete lack of understanding. What I do know, *however*, is how to use the **power of Google**.

---

*time passes by*

---

Well, there's a lot of information out there involving logarithmic math, or machine learning, or both. However, I came across a relatively simple scoring system, where the frequency of letters used in English is broken down by percentage. The percentage is assigned in a dictionary to each letter, and the score is just the sum of the values of all the letters. I like it, it involves minimal math and should be sufficient for this challenge.

Also, it turns out `ETAOIN SHRDLU` is out of date now. The new standard is `ETAOIN SRHLDCU` according to this source: http://norvig.com/mayzner.html

This was used with Google Corpus Data, which means instead of a 20,000 word sample, it's a 743,842,922,321 word sample.
In fact, I'm going to use regular expression to create the dictionary for me. I don't enjoy menial typing, and I do enjoy regular expressions, so let's try it. The below is copy and pasted from the above source:

```
E 445.2 B  12.49%  E
T 330.5 B   9.28%  T
A 286.5 B   8.04%  A
O 272.3 B   7.64%  O
I 269.7 B   7.57%  I
N 257.8 B   7.23%  N
S 232.1 B   6.51%  S
R 223.8 B   6.28%  R
H 180.1 B   5.05%  H
L 145.0 B   4.07%  L
D 136.0 B   3.82%  D
C 119.2 B   3.34%  C
U  97.3 B   2.73%  U
M  89.5 B   2.51%  M
F  85.6 B   2.40%  F
P  76.1 B   2.14%  P
G  66.6 B   1.87%  G
W  59.7 B   1.68%  W
Y  59.3 B   1.66%  Y
B  52.9 B   1.48%  B
V  37.5 B   1.05%  V
K  19.3 B   0.54%  K
X   8.4 B   0.23%  X
J   5.7 B   0.16%  J
Q   4.3 B   0.12%  Q
Z   3.2 B   0.09%  Z
```

Looks easy enough, let's go to our good friend regexr.com

`([A-Z]).+(\d+).(\d+)%` - This will result in 3 capture groups:
1. The percentage number before the decimal.
2. The percentage number after the decimal.
3. The letter.

Since there's no reason to use decimals for scoring since it's simply the sum of these values we can just remove it. Now we can craft the dictionary easily.

In regexr, under list you can reference capture groups like so: `'$3': $1$2, `

This yields: ```
'E': 1249, 'T': 928, 'A': 804, 'O': 764, 'I': 757, 'N': 723, 'S': 651, 'R': 628, 'H': 505, 'L': 407, 'D': 382, 'C': 334, 'U': 273, 'M': 251, 'F': 240, 'P': 214, 'G': 187, 'W': 168, 'Y': 166, 'B': 148, 'V': 105, 'K': 054, 'X': 023, 'J': 016, 'Q': 012, 'Z': 009, ```

Now we just wrap it in curly brackets and remove the last comma and leading zeros:

```python
char_scores = {
'E': 1249, 'T': 928, 'A': 804, 'O': 764, 'I': 757, 'N': 723,'S': 651, 'R': 628, 'H': 505, 'L': 407, 'D': 382, 'C': 334, 'U': 273, 'M': 251, 'F': 240, 'P': 214, 'G': 187, 'W': 168, 'Y': 166, 'B': 148, 'V': 105, 'K': 54, 'X': 23, 'J': 16, 'Q': 12, 'Z': 9}
```

Then create a function which iterates through each character of the string, and returns a result.
This can be accomplished using list comprehension:
```python
return sum([char_scores.get(chr(byte), 0) for byte in input_bytes.upper()])
```

The above statement can be a bit hard to read, let's break it down:

First we have the list comprehension syntax itself. It takes a statement like this:

```python
ordinals = []
for char in 'Hello':
  ordinals.append(ord(char))
```

And turns it into this:
```python
ordinals = [ord(char) for char in 'Hello']
```

Basically you stick the operation on each iteration first, then the for loop second, and wrap it in square brackets to create a list out of it.

So we are iterating though each byte in `input_bytes.upper()`.
The .upper() will translate the byte to the uppercase value of itself. Python is smart enough to know how to upper bytes in relation to their UTF-8 value. You can test it in Idle, python's interactive shell.

```
>>> b'd'.upper()
b'D'
```

The operation being run on each byte is `char_scores.get(chr(byte), 0)`
`chr(byte)` converts the byte value to a single character string using UTF-8 values.

`char_scores.get()` will attempt to retrieve the value assigned to the key with the name of the character, if it's not found it will simply return a 0.
This will take care of decryptions which lead to non-printable characters, or characters not in our scoring dictionary. The second parameter `0` is the value the function should return when the key is not present so that's how it knows to return 0 for those instances.