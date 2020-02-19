from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    username = models.CharField(
        max_length=200,
        verbose_name='Имя пользователя',
        unique=True)
    email = models.EmailField(verbose_name='Адрес электронной почты', unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar')
    following = models.ManyToManyField('self',
                                       through='Contact',
                                       related_name='followers',
                                       symmetrical=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Community(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(Account, related_name='creator_community', on_delete=models.CASCADE)
    img_community = models.ImageField(upload_to='img_community/', blank=True, null=True)

    def __str__(self):
        return self.name


class ConnectCommunityPeople(models.Model):
    users = models.ForeignKey(Account, related_name='users_connect', on_delete=models.CASCADE)
    group = models.ForeignKey(Community, related_name='group_connect', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.group)


class Contact(models.Model):
    user_from = models.ForeignKey(Account,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)     # пользователь-подписчик
    user_to = models.ForeignKey(Account, related_name='rel_to_set',
                                on_delete=models.CASCADE)       # пользователь, на которого подписались
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} подписан на {}'.format(self.user_from, self.user_to)
