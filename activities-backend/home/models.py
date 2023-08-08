from django.db import models

class SidebarMenuItem(models.Model):
    title = models.CharField(max_length=100)
    url   = models.CharField(max_length=200)
    # url   = models.URLField(max_length=512, default=None, null=True, blank=True)

    def __str__(self):
        return self.title
