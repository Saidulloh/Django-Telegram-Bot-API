from django.db import models


class User(models.Model):
    """
    Model for users
    """
    user_id = models.IntegerField(
        verbose_name='user_id'
    )
    first_name = models.CharField(
        max_length=256,
        verbose_name='name',
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=256,
        verbose_name='name',
        null=True,
        blank=True
    )
    username = models.CharField(
        max_length=256,
        verbose_name='username',
        null=True,
        blank=True
    )
    avatarka = models.ImageField(
        upload_to='user_avatars/',
        verbose_name='avatarka',
        null=True,
        blank=True,
        default='admin.png'
    )

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'


class Post(models.Model):
    """
    Model for posts
    """
    title = models.CharField(
        max_length=256,
        verbose_name='post_title'
    )
    image = models.ImageField(
        upload_to='post_images/',
        verbose_name='post_image',
        default='post_images/laptop.png'
    )
    description = models.TextField(
        verbose_name='post_description'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='owner'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'Posts'
