from django.http import JsonResponse
from rest_framework.views import APIView
from .apps import wv_from_text



class Word2Vec(APIView):
    def get(self, request):

        word = request.GET.get('word')

        if word in wv_from_text:
            vec = wv_from_text[word]
            return JsonResponse(vec.tolist(), safe=False)
        else:
            vec = [[1,2],[2,3],[4,5],[7,8],[8,9]]
            return JsonResponse(vec, safe=False)



