from django.db import models
from django.urls import reverse
# Create your models here.
class login(models.Model):
	email = models.TextField(blank=True, null=True)
	pwd   = models.TextField(blank=True, null=True)
	def get(self):
		return reverse("login", kwargs={"id": self.id})

class create(models.Model):
	prompt = models.TextField(blank=False, null=True)
	nb_img = models.IntegerField()
	own_img= models.ImageField()
	def get(self):
		return reverse("create", kwargs={"id":self.id})