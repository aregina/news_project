from utils import DjangoSetup
from db.models import KeyWord, NewsText

if __name__ == "__main__":
    KeyWord.objects.all().delete()
    NewsText.objects.update(is_keywords_extracted=False)
