from rest_framework import serializers

from api.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review. """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        if (self.context.get('request').method == 'POST'
            and Review.objects.filter(title_id=title_id,
                                      author_id=author.id).exists()):
            raise serializers.ValidationError(
                {'detail': 'You have already left a review about this title'})
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
