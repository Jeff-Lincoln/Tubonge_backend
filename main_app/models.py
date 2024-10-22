from django.db import models

class User(models.Model):
    id = models.CharField(max_length=255, unique=True, verbose_name="User ID", primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    image = models.URLField(blank=True, null=True, verbose_name="Profile Image")
    role = models.CharField(max_length=50, default="user", verbose_name="Role")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=['id']),  # Index for 'id' field
        ]


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens', verbose_name="User")
    token = models.CharField(max_length=500, verbose_name="Token")
    validity_in_seconds = models.IntegerField(verbose_name="Validity (in seconds)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Token for {self.user.name}"

    class Meta:
        verbose_name = "User Token"
        verbose_name_plural = "User Tokens"
        indexes = [
            models.Index(fields=['user']),  # Index for ForeignKey 'user'
        ]
