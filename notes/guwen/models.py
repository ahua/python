from django.db import models
from django.contrib import admin
from tinymce.models import HTMLField


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    intro = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "author"

    def __unicode__(self):
        return self.name


class Guwenguanzhi(models.Model):
    id = models.AutoField(primary_key=True)
    vol = models.IntegerField()
    pos = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, default=None, null=True, blank=True)
    finished = models.BooleanField(default=False)
    startdate = models.DateTimeField(blank=True, null=True)
    enddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "guwenguanzhi"

    def __unicode__(self):
        return "%s.%s %s" % (self.vol, self.pos, self.title)

class TinyMce(models.Model):
    id = models.AutoField(primary_key=True)
    content = HTMLField()

class AuthorAdmin(admin.ModelAdmin):
    fields = ('name', 'intro')


class GuwenguanzhiAdmin(admin.ModelAdmin):
    pass


admin.site.register(TinyMce)
admin.site.register(Guwenguanzhi, GuwenguanzhiAdmin)
admin.site.register(Author, AuthorAdmin)
