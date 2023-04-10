from rest_framework import serializers

from flore.models import Image, Plant


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