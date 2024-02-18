import concurrent.futures
import os
from flore.models import Family, Genre, Plant, Image
import json
from datetime import datetime

organ_translation = {
    'fleur': 'flower',
    'feuille': 'leaf',
    'fruit': 'fruit',
    'ecorce': 'bark',
    'port': 'port',
    'rameau': 'branch',
}


def save_file_data(filename):
    json_data = json.load(open("./json_data/" + filename, 'r'))

    for plant_data in json_data.values():
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

            # save plant
            plant = Plant.objects.create(
                id=plant_data['id'],
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
                    date = image_data['date'].split(' ')[0].split('-')
                    if date[-1] == '00':
                        date[-1] = '01'
                    image = Image.objects.create(
                        author=image_data['auteur'],
                        location=image_data['localisation'],
                        publ_date=datetime.strptime('-'.join(date), "%Y-%m-%d"),
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

            percent = (plant_data['id'] * 100) / 171041
            print(plant_data['id'], f"~ {round(percent, 3)}%")

    with open("scripts/logs.json", "+a") as log_file:
        data = json.loads(log_file.read())
        print(data)


def runa():
    data_files = os.listdir('json_data')
    plant_with_images = 0
    image_count = 0
    for filename in data_files:
        json_data = json.load(open("./json_data/" + filename, 'r'))
        if type(json_data) == dict:
            for plant_data in json_data.values():
                if plant_data['images']['organes'] != {} or plant_data['images']['others'] != {}:
                    plant_with_images += 1
                    image_count += len(plant_data['images']['others'])
                    for organ_name, images in plant_data['images']['organes'].items():
                        image_count += len(images)
            print(f"Plants with images: {plant_with_images}")
            print(f"Images count: {image_count}")


def run():
    data_files = os.listdir('json_data')
    print(data_files)
    data_files.sort()
    print(data_files)

    Family.objects.all().delete()
    Genre.objects.all().delete()
    Plant.objects.all().delete()
    Image.objects.all().delete()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(save_file_data, data_files)
