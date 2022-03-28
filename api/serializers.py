from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    # adding this line of code makes the Project Serializer to use the Profile Serializer 
    # whenever it is serializing the owner attribute within the project
    owner = ProfileSerializer(many=False)

    # similarly the ProjectSerializer will now use the TagSerializer to serialize the tags attrbute
    # whenever it is serializing the tags 
    tags = TagSerializer(many=True)

    # using the serializer method fields to return the reviews for each project in the api response
    reviews = serializers.SerializerMethodField() # this is gonna add an attribute just to the serializer

    class Meta:
        model = Project
        fields = '__all__'  
        # if all fields are not required to be serialized, just replace '__all__' with a list of fields

    # the serializer method should start with "get_"
    # the self param refers to the ProjectSerializer and the obj refers to the model we want to serialize (in this case, it is the Project)
    # the final result out of this method is supposed to be returning reviews that are serialized
    def get_reviews(self, obj):
        # obj refers to the model that we are trying to serialize (in this case it refers to the Project)
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    # adding the serializer method field and the method, will automatically add the reviews to the serialized project data
    # that is returned in the views (check the route on the browser)


