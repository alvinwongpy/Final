from django.db import models

class Slider(models.Model):
    slider = models.TextField(blank=True)
    
    def __str__(self):
        s=str(self.slider)
        return "Slider: "+str(self.pk)+"  content:  "+s[0:20]
        