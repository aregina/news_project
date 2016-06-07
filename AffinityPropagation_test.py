print(__doc__)

from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs

from utils import DjangoSetup
import pickle
import sklearn.cluster as s
from db.models import *
import numpy as np
base  = NewsVector.objects.all()[:20000]
vec_base = np.array([pickle.loads(v.vector).toarray()[0] for v in base])


##############################################################################
# Generate sample data
#centers = [[1, 1], [-1, -1], [1, -1]]
#X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5,
#                            random_state=0)

##############################################################################
# Compute Affinity Propagation
af = AffinityPropagation(affinity='euclidean').fit(vec_base)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)

def get_title(n=0):
    for i,v in enumerate(af.labels_):
        if v==n:
            print(i, base[i].news.title)
