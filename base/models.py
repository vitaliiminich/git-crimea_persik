from django.db import models

# Create your models here.

class Month(models.Model):
    title = models.CharField(max_length=50, verbose_name="Месяц созревания")

    def __str__(self):
        return self.title

class Sort(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название сорта")
    short_description = models.TextField(max_length=200, blank=True, verbose_name="Короткое описание")
    full_description = models.TextField(max_length=800, blank=True, verbose_name="Полное описание")
    image = models.ImageField(upload_to="media/images", verbose_name="Изображение")
    mark = models.FloatField(verbose_name="Оценка дегустаторов", default=5)
    cat = models.ForeignKey(Month, on_delete=models.PROTECT, null=True, verbose_name="Срок созревания")

    def __str__(self):
        return self.title

class Faq(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок факта")
    description = models.TextField(max_length=500, verbose_name="Содержание")

    def __str__(self):
        return self.title

class Agreement(models.Model):
    title = models.CharField(max_length=250, verbose_name="Наименование пункта")
    description = models.TextField(max_length=2000, verbose_name="Содержание пункта")

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name="Заголовок статьи")
    image = models.ImageField(upload_to="media/images", verbose_name="Изображение", null=True, blank=True)
    body = models.TextField(verbose_name="Содержание статьи")

    def __str__(self):
        return self.title


#  Модели для связи региона доставки и 
# количества ящиков в зависимости от региона доставки

class Region(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class Amount(models.Model):
    amount = models.CharField(max_length=128)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="amounts")

    def __str__(self):
        return self.amount


    


