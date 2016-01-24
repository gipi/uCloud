# uCloud

Service of cloud storage completely ciphered and privacy aware.

## Implementation

Largely inspired by ``git`` database storage layout: each file is stored with
name given by the **hash** of its own **encrypted content**. The directory
metadata is saved as a ``tree`` that contains the data about the files
permissions; this metadata is also encrypted and saved ith the name given by
the hash of the encypted content of it.

In this way the server doesn't know (at least not immediately) the directory
structure of the files stored.

Since the security of the system is given by the encryption part, that can be
summarized by the encryption key, it should never be communicated with the
server **as is**, all the decryption must be performed client-side. This makes
the possibilty of a web based client a little tricky, maybe we could encrypt
the key with a passphrase and then upload it to the server (to avoid that the
server knows with file is the key, this blob will be uploaded/downloaded at
random).

Maybe could be interesting to split a **blob** into fixed size block and save the
metadata as another tree, i.e., each file is encrypted, splitted into a certain number
of blocks that are saved with the hash of its content and a tree file containing the
ordered list of this blocks is generated.

Also to take into account possible use of salting: prefix each encrypted block with
a n-bits salt (probably is automatically handled by a sane crupto-library).
