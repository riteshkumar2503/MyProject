from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from api_basic.models import ArticleModel1
from api_basic.serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
import json


# REST framework provides two wrappers you can use to write API views. The @api_view decorator for working with function based views. The APIView class for working with class-based views.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated





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



from rest_framework.authtoken.models import Token
# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def function_based_view2(request, pkxyz):
    try:
        one_article = ArticleModel1.objects.get(pk=pkxyz)
        print("one articleeee>>", one_article)
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
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
from rest_framework import generics
from rest_framework import mixins


class GenericView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = ArticleModel1.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'


    def get(self, request, id=None):
        print ("generic view gett", id)
        return self.retrieve(request)
        # if id:
        #     return self.retrieve(request)
        # else:
        #     return self.list(request)

    def post(self, request, id):
        print ("generic view postt")
        return self.create(request)

    def put(self, request, id):
        print ("generic view putt", id)
        return self.update(request, id)

    def delete(self, request, id):
        print ("generic view deletee", id)
        return self.destroy(request, id)










# VIEWSETS *******************************************************
# ViewSet classes are almost the same thing as View classes, except that they provide operations such as retrieve, or update, and not method handlers such as get or put.
# combine the logic for a set of related views in a single class, called a ViewSet. In other frameworks you may also find conceptually similar implementations named something like 'Resources' or 'Controllers'.

from rest_framework import viewsets
from django.shortcuts import get_list_or_404, get_object_or_404

class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):
        print("list aka get all>>")
        all_articles = ArticleModel1.objects.all()
        articles_list_via_seri = ArticleSerializer(all_articles, many=True)
        return Response(articles_list_via_seri.data)

    def create(self, request):
        # print("create aka psot>>", dir(request))
        postdata_via_seri = ArticleSerializer(data=request.data)
        if postdata_via_seri.is_valid():
            postdata_via_seri.save()
            return Response(postdata_via_seri.data, status=status.HTTP_201_CREATED)
        else:
            return Response(postdata_via_seri.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        print ("retrieve aka get one via param>>")
        queryset = ArticleModel1.objects.all()
        # yaha pe ek baar simple try karo
        one_article = get_object_or_404(queryset, pk=pk)
        one_article_seri = ArticleSerializer(one_article)
        return Response(one_article_seri.data)

    def update(self, request, pk=None):
        print ("update11 aka add one via param>>")
        queryset = ArticleModel1.objects.all()
        one_article = get_object_or_404(queryset, pk=pk)
        # direct bhi manga sakte hain neeche wali line ke through..wo jyada better lag raha hai
        # one_article = ArticleModel1.objects.get(pk=pk)
        print ("update22>>")
        one_article_seri = ArticleSerializer(one_article, data=request.data)
        if one_article_seri.is_valid():
            one_article_seri.save()
            return Response(one_article_seri.data)
        else:
            return Response(one_article_seri.errors, status=status.HTTP_400_BAD_REQUEST)


# GENERIC VIEWSETS
# Its like our GenericAPIView. We have to use this with our model mixins
class ArticleGenericViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    # lookup_field = "author"
    queryset = ArticleModel1.objects.all()
    print("xxxx", queryset)
    serializer_class = ArticleSerializer


# MODEL VIEWSETS
class ArticleModelViewSet(viewsets.ModelViewSet):
    queryset = ArticleModel1.objects.all()
    print("cccc", queryset)
    serializer_class = ArticleSerializer





























