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

---

## Decrypting the cipher via XOR

Now that we have a rudimentary english scoring system we can move on to decrypting the cipher.

I accomplished the decryption with the following code:
```python
input = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
input_bytes = bytes.fromhex(input)
decrypted = []

for n in range(256):
    raw = bytearray([byte ^ n for byte in input_bytes])
    score = get_english_score(raw)
    decrypted.append({'score' : score, 'data': raw})

decrypted.sort(key=lambda s: s['score'] , reverse=True)

for i in range(4):
    print(decrypted[i])
```


# Let's break down what each section does.

## Setting up:

```python
input = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
input_bytes = bytes.fromhex(input)
decrypted = []
```

The input value taken from the website has the bytes  extracted and placed into a bytearray object using `bytes.fromhex()`. This allows us to utilize the english scoring function which expects a bytearray to work with. It also allows the XOR operation which is needed to decrypt the cipher.

`decrypted = []` creates a new list object. This will contain each decryption attempt. Since we don't know what value is the correct value to XOR against we have to store each attempt so we can evaluate them based on the english score.

## Brute forcing each possible XOR:

```python
for n in range(256):
    raw = bytearray([byte ^ n for byte in input_bytes])
    score = get_english_score(raw)
    decrypted.append({'score' : score, 'data': raw})
```

The decryption attempts occur in this for loop. We iterate 0 through 255, and during each iteration XOR that value against each byte in the bytearray of the cipher text `input_bytes`. The xor operation occurs using list comprehension, and the resulting list is passed to the `bytearray()` function which converts the xor'd list to a bytearray.

The new bytearray is then passed to our scoring function `get_english_score()`. The result of the score, as well as the new byte array, is appended as a dictionary object to the list of attempted decryptions.

## Sorting the results:
```python
decrypted.sort(key=lambda s: s['score'] , reverse=True)

for i in range(4):
    print(decrypted[i])
```

The sorting can now occur. We are only interested in the highest scoring results. Thankfully Python has a built in way to sort a list. `decrypted.sort(key=lambda s: s['score'] , reverse=True)` , looks kind of complicated but it's required to sort the way we want.

Since each item in our list is a dictionary, we have to tell Python how to properly sort the list. A lambda function is used to keep the code succint. The lambda function does one thing: It returns the value of `score`.

I'll try to keep this explanation brief. Python sees the lambda function passed as the key parameter for the sorting function. The keyword lambda is the required syntax to implement a lambda function. The following `s` is a randomly chosen variable name, it could be anything we like, and it will refer to the current item in the list the sort function is currently processing.

So, the function itself, using s which indicates the current item in the last, will retrieve the value of 'score'. This will return the integer assigned by the scoring function, and sort can process these values and place them in order.

`reverse=True` is a way to have the list sorted from highest value to lowest, which is exactly what we want for this purpose.

The final for loop prints the first 4 items in the decrypted list. I decided to print the first 4 since I know my scoring function won't be compeltely accurate. A list of 4 items is pretty easy to analyze manually as well.

# Getting the answer

Running the script I get the following output:
```
{'score': 15298, 'data': bytearray(b'Ieeacdm*GI-y*fcao*k*ze\x7fdn*el*hkied')}
{'score': 15298, 'data': bytearray(b'iEEACDM\ngi\rY\nFCAO\nK\nZE_DN\nEL\nHKIED')}
{'score': 14223, 'data': bytearray(b"Cooking MC\'s like a pound of bacon")}
{'score': 14223, 'data': bytearray(b'cOOKING\x00mc\x07S\x00LIKE\x00A\x00POUND\x00OF\x00BACON')}
```

Python is nice enough to print the byte arrays as string if it can, escaping non-utf8 values with their hex codes when it cannot translate. We can see the successfully decrypted text, with a score of 14233. There's a pretty similar one right below it, however we can see the spaces and single quotes, as well as the case weren't quite properly decrypted.

In addition, we have two results which actually scored higher than the real result. This means, as I suspected, the most work to be done here lies in the scoring system. Something new to learn, I've already been looking at something called n-grams. For now I'm calling this a success. It's easy enough to look at 4 results and we clearly see the intended message.

# Improving the scoring

After a bit of thinking and playing around I realized a few things:

1. The invalid 3 in the top 4 have no spaces.
2. They all have utf8 codes which aren't representable using alphanumeric or special characters.

I decided to tweak the list to be inclusive by adding spaces, and some select special characeters. I then changed the dictionary get default to `-5000`, which means any decrypted text that has a single character not in our list will take a serious hit to the score. It might be overkill, future use will most likely require adjusments.

I also decided to add a try/except clause, that returns 0 if it cannot decode the bytearray to `utf8`. This will ensure any strings which contain invalid `utf8` values are a flat 0.

I have a feeling I'm going to implement some bigram detection soon, which is the detection of two characters in a row and the likelyhood they are English.

For now, the small updates were sufficient enough to get the correct answer to the top:

```
{'score': 14263, 'data': bytearray(b"Cooking MC\'s like a pound of bacon"), 'key': 88}
{'score': 8041, 'data': bytearray(b"Dhhlni`\'JD t\'knlb\'f\'whric\'ha\'efdhi"), 'key': 95}
{'score': 0, 'data': bytearray(b'\x9b\xb7\xb7\xb3\xb1\xb6\xbf\xf8\x95\x9b\xff\xab\xf8\xb4\xb1\xb3\xbd\xf8\xb9\xf8\xa8\xb7\xad\xb6\xbc\xf8\xb7\xbe\xf8\xba\xb9\xbb\xb7\xb6'), 'key': 128}
{'score': 0, 'data': bytearray(b'\x9a\xb6\xb6\xb2\xb0\xb7\xbe\xf9\x94\x9a\xfe\xaa\xf9\xb5\xb0\xb2\xbc\xf9\xb8\xf9\xa9\xb6\xac\xb7\xbd\xf9\xb6\xbf\xf9\xbb\xb8\xba\xb6\xb7'), 'key': 129}
```