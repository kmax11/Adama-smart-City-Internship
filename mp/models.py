# from django.db import models
# from django.contrib.auth.models import User
# from PIL import Image


from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class Quiz(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     timed = models.BooleanField(default=False)
#     time_limit = models.DurationField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

# class Question(models.Model):
#     quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
#     question_text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.question_text

# class MultipleChoiceOption(models.Model):
#     question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
#     option_text = models.CharField(max_length=255)
#     is_correct = models.BooleanField(default=False)

#     def __str__(self):
#         return self.option_text

# class UserQuizResult(models.Model):
#     user = models.ForeignKey(User, related_name='quiz_results', on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, related_name='quiz_results', on_delete=models.CASCADE)
#     score = models.IntegerField()
#     completed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username}'s result for {self.quiz.title}"

# class userSignUp(models.Model):
#     username = models.CharField(max_length=300)
#     email = models.EmailField()
#     password = models.CharField(max_length=30)
#     confirm = models.CharField(max_length= 30)

#     def __str__(self) -> str:
#         return self.username
    

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#     bio = models.TextField()

#     def __str__(self) -> str:
#         return f'{self.user.username} profile'
#     def save(self):
#         super().save()

#         img = Image.open(self.image.path)
#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)

#             img.thumbnail(output_size)
#             img.save(self.img.path)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_image')

    

        
    def get_url(self):
        return reverse('product_by_category', args=[self.slug])
    def __str__(self) -> str:
        return self.category_name