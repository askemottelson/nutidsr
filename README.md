# nutidsr
A small grammar library for the Danish language

# purpose
Autmatically identify nutids-r errors, e.g., "han styre_ landet".

# how it works
It does pos-tagging (rule based from POS), and tense classification (ML; SVM). From the tense it figures out if you have an error in verb conjucation.

# data
The library relies on two data sets:
* the complete Danish ortography (scraped from dsn.dk; scraper included in lib)
* an annotated data set of tenses of sentences (nutidsr/data.py).
