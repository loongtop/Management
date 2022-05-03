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
    name = models.CharField(verbose_name='COURSE', max_length=32)

    def __str__(self):
        return self.name


class CourseRecord(models.Model):
    """
    CourseRecord
    """
    class_object = models.ForeignKey(verbose_name="ClassList", to="ClassList", on_delete=models.CASCADE)
    day_num = models.IntegerField(verbose_name="Day Num")
    teacher = models.ForeignKey(verbose_name="Teacher", to='Employee', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date", auto_now_add=True)

    def __str__(self):
        return '{self.class_object} day{self.day_num}'


class Student(models.Model):
    nickname = models.CharField(verbose_name='Name', max_length=32)
    phone = models.CharField(verbose_name='Phone', max_length=32)
    emergency_contract = models.CharField(verbose_name='Emergency contact number', max_length=32)
    class_list = models.ManyToManyField(verbose_name="Registered class", to='ClassList', blank=True)
    GENDER_CHOICES = ((1, 'male'), (2, 'female'))
    gender = models.SmallIntegerField(verbose_name='Gender', choices=GENDER_CHOICES, default=1)
    score = models.IntegerField(verbose_name='Point', default=100)


class StudyRecord(models.Model):
    """
    StudyRecord
    """
    course_record = models.ForeignKey(verbose_name="Day of the course", to="CourseRecord", on_delete=models.CASCADE)
    student = models.ForeignKey(verbose_name="Student", to='Student', on_delete=models.CASCADE)
    record_choices = (
        ('normal', "Normal"),
        ('vacate', "On leave"),
        ('late', "Be late"),
        ('absence', "Absence from work"),
        ('leave_early', "Leave early"),
    )
    record = models.CharField(verbose_name="Record of class", choices=record_choices, default="checked", max_length=64)


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


class PointsRecord(models.Model):
    """
    Points record
    """
    student = models.ForeignKey(verbose_name='Student', to='Student', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Reason')
    score = models.IntegerField(verbose_name='Score', help_text='Disciplinary deduction points, good performance bonus points')
    user = models.ForeignKey(verbose_name='Executor', to='Employee', on_delete=models.CASCADE)


class ConsultRecord(models.Model):
    """
    Customer information follow-up records
    """
    customer = models.ForeignKey(verbose_name="Customer", to='Customer', on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name="Recorder", to='Employee', on_delete=models.CASCADE)
    note = models.TextField(verbose_name="Content")
    date = models.DateField(verbose_name="Data", auto_now_add=True)


class PaymentRecord(models.Model):
    """
    payment record
    """
    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name="Consultant", to='Employee', on_delete=models.CASCADE,
                                   help_text="This belongs to who signed the contract")
    pay_type_choices = [
        (1, "registery fee"),
        (2, "tuition fee"),
        (3, "drop out"),
        (4, "others"),
    ]
    pay_type = models.IntegerField(verbose_name="Type", choices=pay_type_choices, default=1)
    paid_fee = models.IntegerField(verbose_name="Amount", default=0)
    class_list = models.ForeignKey(verbose_name="Class", to="ClassList", on_delete=models.CASCADE)
    apply_date = models.DateTimeField(verbose_name="Date", auto_now_add=True)

    confirm_status_choices = (
        (1, 'Applying'),
        (2, 'Confirmed'),
        (3, 'Rejected'),
    )
    confirm_status = models.IntegerField(verbose_name="Status", choices=confirm_status_choices, default=1)
    confirm_date = models.DateTimeField(verbose_name="Date", null=True, blank=True)
    confirm_user = models.ForeignKey(verbose_name="Approver", to='Employee', related_name='confirms',
                                     on_delete=models.CASCADE, null=True, blank=True)

    remark = models.TextField(verbose_name="Remark", blank=True, null=True)












