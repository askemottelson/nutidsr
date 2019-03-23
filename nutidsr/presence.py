from nutidsr.data import annotated
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import numpy as np
from sklearn.preprocessing import StandardScaler
from nutidsr.vectorizer import NutidsrVectorizer
from nutidsr.data import Tid

TEST = True


def make_clf():

    clf = GridSearchCV(
        estimator=Pipeline(
            [
                ("normalize", StandardScaler()),
                # ("reduce_dim", VarianceThreshold()),
                # ("pca", PCA()),
                ("clf", SVC())
            ]
        ),
        param_grid={
            "clf__C": [.01, .05, .1, .5, 1],
            "clf__probability": [True],
            "clf__kernel": ["linear"],
            # "reduce_dim__threshold": [0],
            # "pca__n_components": [2]
        },
        scoring="accuracy"
    )
    return clf


make_clf()


print("load data ...")
# np.random.shuffle(annotated)

train_Xs = []
train_ys = []

test_Xs = []
test_ys = []

vectorizer = NutidsrVectorizer()

vectors = vectorizer.make_all_vector(s[0] for s in annotated)

for i, sentence in enumerate(annotated):
    # 20/80
    if i < len(annotated) / 5:
        # only test 'nutid'
        if sentence[1] == Tid.nutid:
            test_Xs.append(vectors[i])
            test_ys.append(str(sentence[1]))
        else:
            train_Xs.append(vectors[i])
            train_ys.append(str(sentence[1]))
    else:
        train_Xs.append(vectors[i])
        train_ys.append(str(sentence[1]))

print("> done")

train_Xs = np.array(train_Xs)
train_ys = np.array(train_ys)
test_Xs = np.array(test_Xs)
test_ys = np.array(test_ys)

print("train data:", len(train_Xs))
print("test data:", len(test_Xs))

if TEST:

    print("train model ...")

    clf = make_clf()
    clf.fit(train_Xs, train_ys)

    print("> done")
    print("best parameters:")
    print(clf.best_params_)

    print("estimating accuracy ...")

    pred_ys = clf.predict(test_Xs)
    score = f1_score(test_ys, pred_ys, average="weighted")

    print("> done")
    print("f1=", score)


print("train full model ...")

clf = make_clf()
allXs = np.concatenate((train_Xs, test_Xs), axis=0)
allYs = np.concatenate((train_ys, test_ys), axis=0)

clf.fit(allXs, allYs)

print("> done")

print("save model ...")

joblib.dump(clf, 'bin/svm.pkl')
joblib.dump(vectorizer, 'bin/vectorizer.pkl')

print("> done")

print("vocab:")
print(vectorizer.vectorizer.vocabulary_)
