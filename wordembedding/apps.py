from django.apps import AppConfig
# from gensim.models import KeyedVectors

wv_from_text=dict()
class WordembeddingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wordembedding'


    def ready(self):

        # your code here
        # file = r'/Users/wangsiwei/Desktop/workspace/tencent-ailab-embedding-zh-d100-v0.2.0/tencent-ailab-embedding-zh-d100-v0.2.0.txt'
        # print("load wordembedding")
        # global wv_from_text
        # wv_from_text = KeyedVectors.load_word2vec_format(file, binary=False)  # 加载时间比较长
        print("hello")
