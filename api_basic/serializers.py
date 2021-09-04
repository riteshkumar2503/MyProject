from rest_framework import serializers
from api_basic.models import ArticleModel1


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel1
        fields = ('id', 'title', 'author',)
        # fields = '__all__'


# in django terminal do this after creating the serializer
# from api_basic.models import ArticleModel1
# from api_basic.serializers import ArticleSerializer
# articles_list_via_seri = ArticleSerializer(ArticleModel1.objects.all(), many=True)
# print(articles_list_via_seri.data)
# responsejjj = JsonResponse(sss.data, safe=False)  # In order to serialize objects other than dict you must set the safe parameter to False:
# print(responsejjj.data)












# other long way to use serialisers without models

# class ArticleSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     author = serializers.CharField(max_length=100)
#     email = serializers.EmailField(max_length=100)
#     date = serializers.DateTimeField()
#
#     # we need the two below ones if we are using serializers..not if we are using modelserializers
#     def create(self, validated_data):
#         return ArticleModel1.objects.create()
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get(title, instance.title)
#         instance.author = validated_data.get(author, instance.author)
#         instance.email = validated_data.get(email, instance.email)
#         instance.date = validated_data.get(date, instance.date)
#         instance.save()
#         return save