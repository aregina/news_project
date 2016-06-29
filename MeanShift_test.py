import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

###############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)

###############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using

from utils import DjangoSetup
import pickle
import sklearn.cluster as s
from db.models import *
import numpy as np

base  = NewsVector.objects.all()[:200]
vec_base = [pickle.loads(v.vector).toarray()[0] for v in base]

arr = np.ndarray((200,180454))
new_arr = arr+vec_base

bandwidth = estimate_bandwidth(new_arr, quantile=0.5, n_samples=500)


ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(new_arr)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

