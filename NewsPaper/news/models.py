from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):

        rating = 0
        articles = Article.objects.filter(author=self)
        for article in articles:
            rating += article.rating * 3
            rating += article.get_likes()
            rating -= article.get_dislikes()
        comments = Comment.objects.filter(user=self.user)
        for comment in comments:
            rating += comment.rating
        self.rating = rating
        self.save()

    def __str__(self):
        return self.user.username



class Category(models.Model):
        name = models.CharField(max_length=100, unique=True)

        def __str__(self):
            return self.name


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    TYPE_CHOICES = (('article', 'Статья'), ('news', 'Новость'))
    post_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)



    def __str__(self):
        return self.title

    class Author(models.Model):
        name = models.CharField(max_length=255)



    def __str__(self):
        return self.name

    class Category(models.Model):
        name = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    class PostCategory(models.Model):
        post = models.ForeignKey('Post', on_delete=models.CASCADE)

    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} - {self.category.name}'

class PostCategory(models.Model):
        post = models.ForeignKey(Post, related_name='post_categories', on_delete=models.CASCADE)
        category = models.ForeignKey(Category, related_name='category_posts', on_delete=models.CASCADE)

        class Meta:
            unique_together = ('post', 'category')


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    class Post(models.Model):


    def __str__(self):
        return self.title


