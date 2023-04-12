import os
from flore.models import Plant, Image
import json
from datetime import datetime


def run():
    data_files = os.listdir('json_data')

    Plant.objects.all().delete()
    Image.objects.all().delete()

    organ_translation = {
        'fleur': 'flower',
        'feuille': 'leaf',
        'fruit': 'fruit',
        'ecorce': 'bark',
        'port': 'port',
        'rameau': 'branch',
    }

    for file in data_files:
        json_data = json.load(open("./json_data/" + file, 'r'))

        for plant_data in json_data.values():
            if int(plant_data['id']) < 100:
                plant = Plant.objects.create(
                    id=plant_data['id'],
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

                organs = plant_data['images']['organes']
                others_images = plant_data['images']['others']

                for organ_name, images in organs.items():
                    for image_data in images.values():
                        image = Image.objects.create(
                            author=image_data['auteur'],
                            location=image_data['localisation'],
                            publ_date=datetime.strptime(image_data['date'].split(' ')[0], "%Y-%m-%d"),
                            organ=organ_translation[organ_name].upper(),
                            url=image_data['url'],
                            plant=plant
                        )
                        image.save()

                for image_data in others_images.values():
                    image = Image.objects.create(
                            author=image_data['auteur'],
                            location=image_data['localisation'],
                            publ_date=datetime.strptime(image_data['date'].split(' ')[0], "%Y-%m-%d"),
                            organ='NONE',
                            url=image_data['url'],
                            plant=plant
                        )
                    image.save()
            else:
                break

