# uCloud

Service of cloud storage completely encrypted and privacy aware.

** THIS IS A FUCKING EXPERIMENT, DON'T TRY AT HOME **

## Implementation

Largely inspired by ``git`` database storage layout: each file is stored with
name given by the **hash** of its own **encrypted content**. The directory
metadata is saved as a ``tree`` that contains the data about the files
permissions and name; this metadata is also encrypted and saved with the name
given by the hash of the encypted content of it.

In this way the server doesn't know (at least not immediately) the directory
structure of the files stored. In future I would like to study the statistical
distribution of the size of the different kind of blob in order to see if is
possible to deduce from that if a given encrypted content is a directory
metadata related content or a simple little file.

Since the security of the system is given by the encryption part, that can be
summarized by the encryption key, it should never be communicated with the
server **as is**, all the decryption must be performed client-side. This makes
the possibilty of a web based client a little tricky, maybe we could encrypt
the key with a passphrase and then upload it to the server (to avoid that the
server knowns which file is the key, this blob will be uploaded/downloaded at
random).

Maybe could be interesting to split a **blob** into fixed size block and save
the metadata as another tree, i.e., each file is encrypted, splitted into a
certain number of blocks that are saved with the hash of its content and a tree
file containing the ordered list of this blocks is generated. Probably this
splitting is overkilling and also *impossible*: how split a tree?

Also to take into account possible use of salting: prefix each encrypted block
with a n-bits salt (probably is automatically handled by a sane
crypto-library).

## Treat model

No crypto application is complete without a complete threat model, in the
future I will write something about that.

The thing that I would like to create is a storage system that has not
possibilities to infer the filesystem structure of the stored data observing
the exchanged data; probably it's very difficult.
