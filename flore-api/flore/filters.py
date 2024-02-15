from rest_framework import filters


class PlantSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('field_only'):
            return [request.query_params.get('field_only')]
        return ['scientific_name', 'french_name']
