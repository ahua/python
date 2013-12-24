#-*- coding:utf-8 -*-
from django.db import models
from django import forms
import god
from djangotoolbox.fields import ListField


class MultiDBModelAdmin(god.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'mongo'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)


class Testmodel(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

#    class Meta: 
#        verbose_name = '测试类'
#        verbose_name_plural = '测试类'

class TestmodelAdmin(MultiDBModelAdmin):
    list_display = ('name',)

# you'll have to work out how to import the Mongo ListField for yourself :)
class ModelListField(ListField):
    def formfield(self, **kwargs):
        return FormListField(**kwargs)

class ListFieldWidget(forms.SelectMultiple):
    pass

class FormListField(forms.MultipleChoiceField):
    """
    This is a custom form field that can display a ModelListField as a Multiple Select GUI element.
    """
    widget = ListFieldWidget

    def clean(self, value):
    #TODO: clean your data in whatever way is correct in your case and return cleaned data instead of just the value
        return value

class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    tags = ModelListField(models.ForeignKey(Testmodel))
    comments = ModelListField()

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.choices = [(i.pk, i.name) for i in Testmodel.objects.using("mongo").all()]
        if self.instance.pk:
            self.fields['tags'].initial = self.instance.tags

    class Meta:
        model = Post

class PostAdmin(MultiDBModelAdmin):
    form = PostForm
    list_display = ('title', 'text', 'tags', 'comments')
    
    def __init__(self, model, admin_site):
        super(PostAdmin,self).__init__(model, admin_site)

god.site.register(Testmodel, TestmodelAdmin)
god.site.register(Post, PostAdmin)
