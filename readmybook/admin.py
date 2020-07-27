from django.contrib import admin
from .models import Profile, Institue, Book, BooksDB,requestBook
# Register your models here.

admin.site.register(Profile)
admin.site.register(Institue)
admin.site.register(Book)
admin.site.register(BooksDB)
admin.site.register(requestBook)