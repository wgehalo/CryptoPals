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