from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# -----------------------------
# Profile model
# -----------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.user.username} Profile"

# -----------------------------
# Signal: create or update profile automatically when a User is saved
# -----------------------------
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new Profile for the newly created User
        Profile.objects.create(user=instance)
    # Save the profile whenever the User is saved
    instance.profile.save()
