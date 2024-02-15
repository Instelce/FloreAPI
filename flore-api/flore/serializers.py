from rest_framework import serializers

from flore.models import Family, Genre, Image, Plant


class PlantFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['id', 'name']


class PlantGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class WritePlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
            'num_inpn',
            'rank_code',
            'family',
            'genre',
            'scientific_name',
            'correct_name',
            'french_name',
            'author',
            'publ_year',
            'eflore_url'
        ]


class ReadPlantSerializer(serializers.ModelSerializer):
    family = serializers.SlugRelatedField(slug_field='name', queryset=Family.objects.all())
    genre = serializers.SlugRelatedField(slug_field='name', queryset=Genre.objects.all())

    class Meta:
        model = Plant
        fields = [
            'id',
            'num_inpn',
            'rank_code',
            'family',
            'genre',
            'scientific_name',
            'correct_name',
            'french_name',
            'author',
            'publ_year',
            'eflore_url'
        ]
        read_only_fields = fields


class WriteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'author',
            'location',
            'publ_date',
            'organ',
            'url',
            'plant'
        ]


class ReadImageSerializer(serializers.ModelSerializer):
    plant = ReadPlantSerializer()

    class Meta:
        model = Image
        fields = [
            'id',
            'author',
            'location',
            'publ_date',
            'organ',
            'url',
            'plant'
        ]
        read_only_fields = fields


class ReadImageNoPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'author',
            'location',
            'publ_date',
            'organ',
            'url',
        ]
        read_only_fields = fields


class PlantImagesSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    images = serializers.ListField(
        child=ReadImageNoPlantSerializer(),
    )


class CompletePlantImagesSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=ReadImageNoPlantSerializer(),
    )

    class Meta:
        model = Plant
        fields = [
            'id',
            'num_inpn',
            'rank_code',
            'family',
            'genre',
            'scientific_name',
            'correct_name',
            'french_name',
            'author',
            'publ_year',
            'eflore_url',
            'images'
        ]
        read_only_fields = fields

