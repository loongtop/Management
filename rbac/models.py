from django.db import models


# Create your models here.


class Role(models.Model):
    """Role"""
    title = models.CharField(verbose_name='title', max_length=64)
    permission = models.ForeignKey(verbose_name='permission', to='Permission', max_length=32, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class User(models.Model):
    """This class can be used as a "parent class" that is inherited by other Model classes"""
    name = models.CharField(verbose_name='name', max_length=64)
    password = models.CharField(verbose_name='password', max_length=64)
    email = models.CharField(verbose_name='email', max_length=64)
    role = models.ManyToManyField(verbose_name='Role', to=Role, max_length=32, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # When django does database migration in the future,
        # it will no longer create related tables and table structures for the UserInfo class.
        abstract = True


class Permission(models.Model):
    """Permission"""
    title = models.CharField(verbose_name='title', max_length=64)
    alias = models.CharField(verbose_name='Alias', max_length=64, unique=True)
    url = models.CharField(verbose_name='URL with RE', max_length=128)
    parent_id = models.ForeignKey(verbose_name='Parent ID', to='Permission', max_length=32, on_delete=models.CASCADE,
                                  null=True, blank=True, related_name='parents',
                                  help_text='non-menu permissions and menu permissions')
    menu = models.ForeignKey(verbose_name='To Menu', to='Menu', null=True, blank=True, on_delete=models.CASCADE,
                             help_text='null means not a menu; non-null means it is a secondary menu')

    def __str__(self):
        return self.title


class Menu(models.Model):
    """
    Menu
    """
    title = models.CharField(verbose_name='title', max_length=32)
    icon = models.CharField(verbose_name='icon', max_length=32)

    def __str__(self):
        return self.title
