from django.db import models


class Plant(models.Model):
    num_inpn = models.CharField(default='', max_length=9)
    rank_code = models.CharField(default='', max_length=9)

    family = models.CharField(default='', max_length=100)
    genre = models.CharField(default='', max_length=100)

    scientific_name = models.CharField(default='', max_length=500)
    correct_name = models.CharField(default='', max_length=500)
    french_name = models.CharField(default='', max_length=500)

    author = models.CharField(default='', max_length=100)
    publ_year = models.CharField(default='', max_length=4)
    eflore_url = models.URLField(default='')

    class Meta:
        ordering = ['scientific_name']


class Image(models.Model):
    ORGAN_CHOICES = (
        ('NONE', 'none'),
        ('FLOWER', 'flower'),
        ('LEAF', 'leaf'),
        ('FRUIT', 'fruit'),
        ('BARK', 'bark'),
        ('PORT', 'port'),
        ('BRANCH', 'branch'),
    )
    author = models.CharField(default='', max_length=100)
    location = models.CharField(default='', max_length=500)
    publ_date = models.DateField(default='')
    organ = models.CharField(choices=ORGAN_CHOICES, default='NONE', max_length=10)
    url = models.URLField(blank=False)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
