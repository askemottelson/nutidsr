from sklearn.externals import joblib
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nutidsr.data import Tid

clf = joblib.load('bin/svm.pkl') 
vectorizer = joblib.load('bin/vectorizer.pkl') 


def predict(s):
    X = vectorizer.make_vector(s)
    if np.sum(X) < 1:
        return "-1", 0.0

    r = clf.predict(X)[0]
    conf = clf.predict_proba(X)[:,1][0]
    #is_nutid = r == str(Tid.nutid)
    return r, conf

print(predict("jeg går mig en tur"))
print(predict("jeg gik mig en tur"))
print(predict("jeg styrer det hele"))
print(predict("jeg styre det hele"))

print(predict("en katastrofisk kurs sat af de ledende skikkelser"))
print(predict("akademiet flytter posterne i endnu ukendt præcision"))
print(predict("akademiet spiser posterne i endnu ukendt præcision"))
print(predict("this sentence is not even Danish"))