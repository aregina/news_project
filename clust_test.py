from utils import DjangoSetup
import pickle
import sklearn.cluster as s
from db.models import *

base  = NewsVector.objects.all()[:200]

clus = s.KMeans(30)

vec_base = [pickle.loads(v.vector).toarray()[0] for v in base]

clus.fit(vec_base)

print(clus.labels_)


def get_title(n=0):
    for i,v in enumerate(clus.labels_):
        if v==n:
            print(base[i].news.title)

get_title()
            
