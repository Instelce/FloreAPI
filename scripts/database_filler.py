import os
from flore.models import Family, Genre, Plant, Image
import json
from datetime import datetime


def run():
    data_files = os.listdir('json_data')

    Family.objects.all().delete()
    Genre.objects.all().delete()
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
            # if int(plant_data['id']) < 200: # For test, else, remove this line

            # if the plant has images
            if plant_data['images']['organes'] != {} or plant_data['images']['others'] != {}:
                # Create family and genre if they don't exists
                if plant_data['famille'] not in [family.name for family in Family.objects.all()]:
                    family = Family.objects.create(name=plant_data['famille'])
                    family.save()
                else:
                    family = Family.objects.get(name=plant_data['famille'])
                if plant_data['genre'] not in [genre.name for genre in Genre.objects.all()]:
                    genre = Genre.objects.create(name=plant_data['genre'])
                    genre.save()
                else:
                    genre = Genre.objects.get(name=plant_data['genre'])

                plant = Plant.objects.create(
                    #id=plant_data['id'],
                    num_inpn=plant_data['num_inpn'],
                    rank_code=plant_data['code_rang'],
                    family=family,
                    genre=genre,
                    scientific_name=plant_data['nom_scientifique'],
                    correct_name=plant_data['nom_retenu'],
                    french_name=plant_data['french_name'] if "french_name" in plant_data else "",
                    author=plant_data['auteur'],
                    publ_year=plant_data['annee_publ'],
                    eflore_url=plant_data['url'],
                )
                plant.save()

                # Images of classified organs
                organs = plant_data['images']['organes']
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

                # Others images
                others_images = plant_data['images']['others']
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

                print(plant.scientific_name, plant.num_inpn)
            # else:
            #     break

