from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Institue(models.Model):
    name = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20, default='')
    lastName = models.CharField(max_length=20, default='')
    college = models.CharField(max_length=20, default='')
    bio = models.CharField(max_length=200, default='Hey, I am new here')
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # imp shit here

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='book_cover/', default='book.png')

    def __str__(self):
        return self.name


class BooksDB(models.Model):
    status_choices=(
        ('available', 'available'),
        ('notavailable','notavailable')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    status=models.CharField(max_length=20, choices=status_choices, default='available')
    def __str__(self):
        return f'{self.book.name} | Owned: {self.owner.username}'


class requestBook(models.Model):
    status_choice = (
        ("pending", "pending"),
        ("received-pen", "received"),
        ("returned-pen", "returned"),
        ("completed", "completed"),
        ("cancelled", "cancelled"),
    )

    status_c = (
        ('pending', 'pending'),
        ('done', 'done')
    )
    request_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_to')
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_by')
    book = models.ForeignKey(BooksDB, on_delete=models.CASCADE)
    status = models.CharField(choices=status_choice, max_length=20, default='pending')
    by_status = models.CharField(choices=status_c, max_length=20, default='pending')
    to_status = models.CharField(choices=status_c, max_length=20, default='pending')

    def __str__(self):
        return f'{self.book.book.name} | by: {self.request_by.username} | to: {self.request_to.username}'
