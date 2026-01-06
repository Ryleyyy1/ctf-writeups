# PicoCTF — bases

## Category
General Skills

## Description
The challenge provides an encoded string and hints that it uses
number-based encodings.

The task is to decode the string and retrieve the flag.

---

## Analysis
By examining the character set of the encoded string, it matches
the standard Base64 format:

- Uppercase & lowercase letters
- Numbers
- `=` padding

Thus, the encoding is identified as **Base64**.

---

## Solution
Instead of decoding manually, Python's built-in `base64` module
was used to decode the string.

---

## Result
Decoded output:
picoCTF{l3arn_th3_r0p35}
