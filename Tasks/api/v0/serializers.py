from rest_framework import serializers
from rest_framework.response import Response
from Tasks.models import Task, Category
from Accounts.models import Profile

## Create your serializers here
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    author = serializers.SlugRelatedField(read_only=True, slug_field='profile_user__email')
    # importance = serializers.CharField(source='get_importance_display')
    # status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Task
        fields = ['id','author', 'title', 'status', 'category', 'importance', 'created_date',
                  'edited_date', 'completed_date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            profile = Profile.objects.get(profile_user=request.user)
            self.fields['category'].queryset = Category.objects.filter(creator=profile)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        # remove some fields in list data and add them in single data details
        if request.parser_context.get('kwargs').get('pk'): #this if statement determines our request is for getting a single object or a list of objects
            representation
        else:
            not_show_fields = ['id', 'created_date', 'edited_date', 'completed_date']
            for field in not_show_fields:
                representation.pop(field)
        representation['category'] = CategorySerializer(instance.category).data #show both id & name of foriegnkey field
        
        # Dynamically swap out the short codes for the human-readable labels
        representation['importance'] = instance.get_importance_display()
        representation['status'] = instance.get_status_display()
        return representation

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(profile_user=self.context.get('request').user)
        return super().create(validated_data)