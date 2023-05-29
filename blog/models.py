from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from PIL import Image
import os

class Category(models.Model):
    title = models.CharField(max_length=32, verbose_name=u'Tytuł')
    slug = models.SlugField(max_length=32, verbose_name=u'Odnośnik')
    opisc = models.TextField(max_length=300, verbose_name=u'Opis Kategorii', blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Kategorie'

    def save(self, *args, **kwargs):
        if not self.opisc:  # Jeśli pole 'opisc' jest puste
            self.opisc = self.title  # Ustawiamy wartość 'opisc' na wartość z 'title'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug

class Tag(models.Model):
    title = models.CharField(max_length=32, verbose_name=u'Tytuł')
    slug = models.SlugField(max_length=32, verbose_name=u'Odnośnik')
    opist = models.TextField(max_length=300, verbose_name=u'Opis Tagu', blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Tagi'

    def save(self, *args, **kwargs):
        if not self.opist:  # Jeśli pole 'opist' jest puste
            self.opist = self.title  # Ustawiamy wartość 'opist' na wartość z 'title'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/tag/%s/' % self.slug

class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'
    CHOICES_STATUS = ((ACTIVE, 'Active'), (DRAFT, 'Draft'))
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, verbose_name=u'Kategoria')
    title = models.CharField(max_length=62, verbose_name=u'Tytuł')
    slug = models.SlugField(max_length=32, verbose_name=u'Odnośnik')
    autor = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    body = models.TextField(verbose_name=u'Treść')
    pub_date = models.DateTimeField(auto_now_add=False, verbose_name=u'Data Publikacji')
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Strona', null=True)
    tags = models.ManyToManyField('Tag', verbose_name=u'Tagi', blank=True)
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='Obraz', null=True, help_text='Image Only: JPG, JPEG, PNG, WebP.')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Artykuły'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%s.html' % (self.category.slug, self.slug)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            max_width = 900
            if img.width > max_width:
                ratio = max_width / img.width
                height = int(img.height * ratio)
                img.thumbnail((max_width, height))

            # Konwersja do formatu WebP (jeśli nie jest już w tym formacie)
            if not self.image.name.lower().endswith('.webp'):
                webp_path = os.path.splitext(self.image.path)[0] + '.webp'
                img.save(webp_path, 'WEBP')
                self.image.name = os.path.splitext(self.image.name)[0] + '.webp'
                self.save()  # Zapisz obiekt ponownie, aby zaktualizować pole image

    def delete(self, *args, **kwargs):
        if self.image:
            webp_path = os.path.splitext(self.image.path)[0] + '.webp'
            if os.path.exists(webp_path):
                os.remove(webp_path)
            default_storage.delete(self.image.name)  # Usuń również oryginalny plik JPG
        super().delete(*args, **kwargs)

    def get_image_alt(self):
        if self.image:
            file_name = os.path.basename(self.image.name)
            return os.path.splitext(file_name)[0]  # Pobierz nazwę pliku bez rozszerzenia
        return ''

    def get_image_title(self):
        return self.get_image_alt()
