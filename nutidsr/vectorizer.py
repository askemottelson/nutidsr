from sklearn.feature_extraction.text import CountVectorizer
from nutidsr.sentence import Sentence
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import difflib

class NutidsrVectorizer():

    vectorizer = None

    def extract_words(self, sentence):
        s = Sentence(sentence.split())
        objs, words = s.get_all(), s.sentence
        verbs = []
        for obj, word in zip(objs, words):
            if obj and obj.category in ['vb.', 'pron.', 'konj.']:
                verbs.append(word)

                # experimental; add the string diff as a feature
                plus_letters = []
                for d in difflib.ndiff(obj.word, word):
                    if d[0] == '+':
                        plus_letters.append(d[-1])
                if len(plus_letters) > 0:
                    verbs.append('+' + "".join(plus_letters))

        return verbs

    def make_all_vector(self, sentences):
        self.vectorizer = CountVectorizer(
            strip_accents="unicode",
            lowercase=True,
            analyzer="word",
            token_pattern=r"(?u)[a-zæøå\-\+]+"
        )

        corpus = []
        for sentence in sentences:
            words = self.extract_words(sentence)
            corpus.append(" ".join([w for w in words]))

        X = self.vectorizer.fit_transform(corpus)

        return X.toarray().astype(float)

    def make_vector(self, sentence):
        words = " ".join(self.extract_words(sentence))
        X = self.vectorizer.transform([words])
        return X.toarray().astype(float)


if __name__ == "__main__":
    from nutidsr.data import annotated 
    vec = NutidsrVectorizer()
    X = vec.make_all_vector([s[0] for s in annotated])
    cs = [int(s[1]) for s in annotated]    

    pca = PCA(n_components=2)
    X_r = pca.fit(X).transform(X)

    xs = [x[0] for x in X_r]
    ys = [x[1] for x in X_r]

    colors = np.array(['red','blue','green','yellow','orange'])

    plt.scatter(xs, ys, color=colors[cs], alpha=.25)
    plt.show()