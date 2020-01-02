
# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    
    mobile_no = models.IntegerField(null=True)
    work_no = models.IntegerField(null=True)
    other_no = models.IntegerField(null=True)

    customer_email = models.EmailField(max_length=254,null=True)
    depart_date= models.DateTimeField(null=True)
    return_date=models.DateTimeField(null=True)

    booked = models.IntegerField(default=1)

    remarks = models.TextField(null=True)
    
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
