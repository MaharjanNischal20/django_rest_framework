from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogs')
    title = models.CharField(max_length=100)
    blog_text = models.TextField()  
    main_image = models.ImageField(upload_to="blogs")

    def __str__(self):
        return self.title