from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self, email, student_id, department, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, student_id=student_id, department=department, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, student_id, department, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, student_id, department, phone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=100, default="Unknown")  # 🔥 기본값 추가
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_id', 'department', 'phone','name']

    def __str__(self):
        return self.email

User = get_user_model()

class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 동아리 이름
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="led_club")  # 동아리장 (유저)
    advisor = models.CharField(max_length=100)  # 지도 교수
    max_members = models.PositiveIntegerField()  # 최대 인원수
    current_members = models.PositiveIntegerField(default=0)  # 현재 인원수
    activity_schedule = models.CharField(max_length=200)  # 활동 일정
    tags = models.CharField(max_length=255, blank=True)  # 태그 (콤마로 구분된 문자열)
    description = models.TextField(blank=True)  # 동아리 소개
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)  # 🔥 추가된 부분
    def __str__(self):
        return self.name
