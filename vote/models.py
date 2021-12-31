from django.db import models
from acc.models import User

# Create your models here.
class Topic(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vwriter")
    pubdate = models.DateTimeField()
    content = models.TextField()
    voter = models.ManyToManyField(User, blank=True, related_name="voter")

    def __str__(self):
        return self.subject
    
    def summary(self):
        if len(self.content) > 10:
            return self.content[:10] + "..."
        return self.content

class Choice(models.Model):
    subject = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="vote/%y")
    comment = models.TextField()
    choicer = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"



