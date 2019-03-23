# nutidsr
A small grammar library for Danish

# purpose
Autmatically identify nutids-r errors, e.g., "han styre_ landet".

# how it works
It does pos-tagging (rule based from POS), and tense classification (ML; SVM). From the tense it figures out if you have an error in verb conjucation.
