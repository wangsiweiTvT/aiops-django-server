from django.urls import path
from .views import Word2Vec
app_name = 'wordembedding'
urlpatterns = [
    path(r'word2vec/', Word2Vec.as_view()),
]
# import openai
#
# openai.api_base = "https://baichuan2-api-zdm.smzdm.com/v1"
# openai.api_key = "xxx"
# completion = openai.ChatCompletion.create(
#     model="baichuan2-13b-chat",
#     messages=[
#         {"role": "user", "content": "how are you"},
#     ],
#     stream=False,
# )
#
# print(completion.choices[0].message.content)