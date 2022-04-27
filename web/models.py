from django.db import models

# Create your models here.


class Employee(models.Model):
    """
    the table of the Employee
    """
    nickname = models.CharField(verbose_name='Name', max_length=32)
    phone = models.CharField(verbose_name='Phone', max_length=32)
    GENDER_CHOICES = ((1, 'male'), (2, 'female'))
    gender = models.SmallIntegerField(verbose_name='Gender', choices=GENDER_CHOICES, default=1)
    department = models.ForeignKey(verbose_name='department', to='Department', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nickname


class Department(models.Model):
    """
    the table of the department
    """
    title = models.CharField(verbose_name='Name', max_length=32)

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    the table of the Course
        Chinese, English, French, Russian, Japanese, Korean, Spanish, German
    """
    name = models.CharField(verbose_name='Course', max_length=32)

    def __str__(self):
        return self.name


class Student(models.Model):
    nickname = models.CharField(verbose_name='Name', max_length=32)
    phone = models.CharField(verbose_name='Phone', max_length=32)
    emergency_contract = models.CharField(verbose_name='Emergency contact number', max_length=32)
    class_list = models.ManyToManyField(verbose_name="Registered class", to='ClassList', blank=True)
    GENDER_CHOICES = ((1, 'male'), (2, 'female'))
    gender = models.SmallIntegerField(verbose_name='Gender', choices=GENDER_CHOICES, default=1)
    score = models.IntegerField(verbose_name='Point', default=100)


class Customer(models.Model):
    """
    the table of the Customer
    """
    MAX_PRIVATE_COUNT = 150
    name = models.CharField(verbose_name='Name', max_length=32)
    email = models.CharField(verbose_name='', max_length=64, unique=True, help_text='QQ号/微信/手机号')
    phone = models.CharField(verbose_name='', max_length=64, unique=True, help_text='QQ号/微信/手机号')
    STATUS_CHOICES = [
        (1, "Registered"),
        (2, "Not registered")
    ]
    status = models.IntegerField(verbose_name="状态", choices=STATUS_CHOICES, default=2)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    SOURCE_CHOICES = [
        (1, "Friends"),
        (2, "Official Web"),
        (3, "Advisement"),
        (4, "Others"),
    ]
    source = models.SmallIntegerField('Source', choices=SOURCE_CHOICES, default=1)

    course = models.ManyToManyField(verbose_name="Course", to="Course")

    def __str__(self):
        return f'Name:{self.name}, Phone:{self.phone}'


class School(models.Model):
    """
    the table of the SchoolArea:

        Dongcheng District, Xicheng District, Chaoyang District, Fengtai District, Shijingshan District,
        Haidian District, Shunyi District, Tongzhou District, Daxing District, Fangshan District,
        Mentougou District, Changping District, Pinggu District, Miyun District, Huairou District, Yanqing District
    """
    title = models.CharField(verbose_name='Campus', max_length=32)

    def __str__(self):
        return self.title


class ClassList(models.Model):
    """
    the table of the ClassTable:

    """
    school = models.ForeignKey(verbose_name='School', to='School', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(verbose_name='Course', to='Course', on_delete=models.DO_NOTHING)
    semester = models.PositiveIntegerField(verbose_name="Term")
    price = models.PositiveIntegerField(verbose_name="Price")
    start_date = models.DateField(verbose_name="Start Date")
    graduate_date = models.DateField(verbose_name="Finish Date", null=True, blank=True)
    # limit_choices_to = 'department__title': ''
    class_teacher = models.ForeignKey(verbose_name='Class Teacher', to='Employee',
                                      related_name='classes', on_delete=models.DO_NOTHING)
    # limit_choices_to = {'depart__title__in': ['Linux教学部', 'Python教学部'
    tech_teachers = models.ManyToManyField(verbose_name='Teacher', to='Employee',
                                           related_name='teach_classes', blank=True)
    memo = models.TextField(verbose_name='Memo', blank=True, null=True)

    def __str__(self):
        return f"{self.course.name}({self.semester} term)"












