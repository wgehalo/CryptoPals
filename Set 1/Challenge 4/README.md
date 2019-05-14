# Challenge 4: Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)

---

# Walkthrough

This one seems simple enough. Essentially it's taking the code we created in the last challenge and putting it to practical use.

We will utilize the code with some adjustments to read the file of ciphers, and iterate through each one. We will keep the top 4 from each attempted decryption, append those to a master list, and keep the top 4 of that list.

## Some new stuff has been introduced into this code, let's take a closer look:


### Slicing a list:
```python
del decrypted[5:-1]
```
This is how you slice a list in python. `del` is short for delete, `decrypted` is the list we are deleting from, and `[5:-1]` references the index range to delete.

In python you can reference the last index of a list using the value `-1`, it's extremely handy.

### Setting the right path for a file:
```python
script_dir = os.path.dirname(os.path.realpath(__file__))
input_fd = os.path.join(script_dir, '4.txt')
```

There are lots of built in functions which support file path manipulation contained within the standard os library. `os.path.realpath` will return the actual path of a given file, eliminating any symbolic links along the way.

Explaining symbolic links is beyond the scope of this project, all we need to know is this function will get us the absolute path of any given file.

`__file__` is a built in variable in python which references the file it is currently in. In our instance it references `needle_in_haystack.py`. Since we are passing this to the `realpath` function it will return the full path, whatever it may be on the system running the script.

`os.path.dirname()` will return the directory name of a given file, which is exactly what we are after. When someone clones this git repository, we don't know where they are going to store it, however we know the file `4.txt` will reside in the same folder as the `need_in_haystack.py`. Using this function we can get the full directory name of where `4.txt` will reside even if it's 15 subfolders deep.

`os.path.join()` is a very useful function for building cross platform file paths. Windows and Linux don't create paths the same way, however if we us this function python will craft the correct directory structure regardless of the environment.


### Reading from a file:
```python
with open(input_fd, 'r') as f:
    for line in f:
        master_list += (attempt_decryption(line))
```

Now that we have a valid filepath which should work no matter what environment it's run in, we can use `open()` to read the file. Using `with` will ensure the file stream is closed after we are done with it, otherwise we would have to remember to close the file manually after opening it. We set the variable name after the `as` statement, with `f` being a standard convention for file.

`for line in f:` will iterate through each line in the file. Python is pretty slick in this regard and makes it extremely simple to iterate line by line through a text file. The rest is just adding the top 4 elements from each decryption attempt to our master list.

### Revisiting sorting:
```python
master_list.sort(key=lambda s: s['score'], reverse=True)

for i in range(4):
    print(master_list[i])
```

This last bit is the same as the end of the previous challenge, it just uses the master_list which has the top 4 scores from each attempt instead of a single attempt.

# Running the script

```
{'score': 9101, 'data': bytearray(b'Now that the party is jumping\n'), 'key': 53, 'line': 171}
{'score': 171, 'data': bytearray(b'Jks$plep$pla$tevp}$mw$nqitmjc\x0e'), 'key': 49, 'line': 171}
{'score': 0, 'data': bytearray(b"\x0e6G\xe8Y-5QJ\x08\x12CX%6\xed=\xe6s@Y\x00\x1e?S\\\xe6\'\x102"), 'key': 0, 'line': 1}
{'score': 0, 'data': bytearray(b'\x0f7F\xe9X,4PK\t\x13BY$7\xec<\xe7rAX\x01\x1f>R]\xe7&\x113'), 'key': 1, 'line': 1}
```
And there we have it, `line 171` has been xor'd with a byte value of `53`.

Also, it looks like the scoring system is holding up so far.

# :tada::tada::tada::tada: