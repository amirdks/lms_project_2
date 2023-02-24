from rest_framework.serializers import ModelSerializer

from lesson_module.models import Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title']
