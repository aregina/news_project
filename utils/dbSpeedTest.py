from utils import DjangoSetup
from db.models import Site
from django.db import transaction
from time import time


@transaction.atomic
def add_to_base(n):
    for i in range(n):
        Site.objects.create(name='ffff')


@transaction.atomic
def del_from_base():
    for i in Site.objects.iterator():
        if i.name == 'ffff':
            i.delete()


if __name__ == "__main__":
    start = time()
    add_to_base(10000)
    end1 = time() - start
    del_from_base()
    end2 = time() - start - end1
    print("Add in base {}\nDel from base {}".format(end1, end2))
