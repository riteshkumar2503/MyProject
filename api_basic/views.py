from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from api_basic.models import ArticleModel1
from api_basic.serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt

# REST framework provides two wrappers you can use to write API views. The @api_view decorator for working with function based views. The APIView class for working with class-based views.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status




# FUNCTION BASED VIEW **************************************************************************
# @csrf_exempt  # Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to mark the view as csrf_exempt. This isn't something that you'd normally want to do
@api_view(['GET', 'POST'])
def function_based_view(request):
    if request.method == 'GET':
        all_articles = ArticleModel1.objects.all()
        articles_list_via_seri = ArticleSerializer(all_articles, many=True)
        # return JsonResponse (articles_list_via_seri.data, safe=False)  # In order to serialize objects other than dict you must set the safe parameter to False:
        return Response (articles_list_via_seri.data)



    elif request.method == 'POST':
        # data123 = JSONParser().parse(request)
        # postdata_via_seri = ArticleSerializer(data=data123)
        postdata_via_seri = ArticleSerializer(data=request.data)  #instead of above two lines
        if postdata_via_seri.is_valid():
            postdata_via_seri.save()
            return Response(postdata_via_seri.data, status=status.HTTP_201_CREATED)
        else:
            return Response(postdata_via_seri.errors, status=status.HTTP_400_BAD_REQUEST)




# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def function_based_view2(request, pkxyz):
    try:
        one_article = ArticleModel1.objects.get(pk=pkxyz)
        print("eee", one_article)
    except ArticleModel1.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        one_article_seri = ArticleSerializer(one_article)
        return Response(one_article_seri.data)

    elif request.method == 'PUT':
        # data123 = JSONParser().parse(request)
        putdata_seri = ArticleSerializer(one_article, data=request.data)  # pass in the instance we want to update
        if putdata_seri.is_valid():
            putdata_seri.save()
            return Response(putdata_seri.data)
        else:
            return Response(putdata_seri.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print("fff")
        one_article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










# CLASS BASED VIEW *******************************************************
# https://stackoverflow.com/questions/14788181/class-based-views-vs-function-based-views
from rest_framework.views import APIView


class ClassBasedView(APIView):
    def get(self, request):
        all_articles = ArticleModel1.objects.all()
        articles_list_via_seri = ArticleSerializer(all_articles, many=True)
        return Response (articles_list_via_seri.data)

    def post(self, request):
        postdata_via_seri = ArticleSerializer(data=request.data)
        if postdata_via_seri.is_valid():
            postdata_via_seri.save()
            return Response(postdata_via_seri.data, status=status.HTTP_201_CREATED)
        else:
            return Response(postdata_via_seri.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassBasedView2(APIView):
    def get_one_object(self, pkxyz):
        try:
            print("wwwwww")
            return ArticleModel1.objects.get(pk=pkxyz)
        except ArticleModel1.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pkxyz):
        print("ddddddddddd")
        one_article = self.get_one_object(pkxyz)
        one_article_seri = ArticleSerializer(one_article)
        return Response(one_article_seri.data)

    def put(self, request, pkxyz):
        one_article = self.get_one_object(pkxyz)
        putdata_seri = ArticleSerializer(one_article, data=request.data)  # pass in the instance we want to update
        if putdata_seri.is_valid():
            putdata_seri.save()
            return Response(putdata_seri.data)
        else:
            return Response(putdata_seri.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pkxyz):
        one_article = self.get_one_object(pkxyz)
        one_article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# GENERIC VIEWS *******************************************************
#  ListModelMixin Provides a .list(request, *args, **kwargs) method, that implements listing a queryset. If the queryset is populated, this returns a 200 OK response, with a serialized representation of the queryset as the body of the response. The response data may optionally be paginated.
# CreateModelMixin Provides a .create(request, *args, **kwargs) method, that implements creating and saving a new model instance
from rest_framework import generics
from rest_framework import mixins


class GenericView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = ArticleModel1.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        print ("generic view gett", id)
        if id:
            return self.retrieve(request)
        else:
            print ("generic view getttttt", id)
            return self.list(request)

    def post(self, request, id):
        print ("generic view postt")
        return self.create(request)

    def put(self, request, id):
        print ("generic view putt", id)
        return self.update(request, id)

    def delete(self, request, id):
        print ("generic view deletee", id)
        return self.destroy(request, id)





















