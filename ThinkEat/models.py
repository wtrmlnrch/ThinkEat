from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

CustomUser = get_user_model()

class SavedRecipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_recipes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} saved by {self.user.username}"