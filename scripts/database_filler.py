import os
from flore.models import Plant, Image
import json


def run():
    data_files = os.listdir('json_data')

    Plant.objects.all().delete()
    Image.objects.all().delete()

    for file in data_files:
        json_data = json.load(open("./json_data/" + file, 'r'))

        for plant_data in json_data.values():
            if int(plant_data['id']) < 100:
                # Add new plant to database
                plant = Plant(
                    num_inpn=plant_data['num_inpn'],
                    rank_code=plant_data['code_rang'],
                    family=plant_data['famille'],
                    genre=plant_data['genre'],
                    scientific_name=plant_data['nom_scientifique'],
                    correct_name=plant_data['nom_retenu'],
                    french_name=plant_data['french_name'] if plant_data['french_name'] != None else "",
                    author=plant_data['auteur'],
                    publ_year=plant_data['annee_publ'],
                    eflore_url=plant_data['url'],
                )
                plant.save()
                print(plant.scientific_name)
            else:
                break

