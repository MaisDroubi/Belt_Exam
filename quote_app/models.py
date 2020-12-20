from django.db import models
from login_regist_app import models as login_models

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if postData['author'] == "":
            errors['author'] = "Please enter an author."
        elif len(postData['author']) < 3:
            errors['author'] = "Author name must be greater than 3 characters."
        if postData['quote'] == "":
            errors['quote'] = "Please enter a quote."
        elif len(postData['quote']) < 10 or len(postData['quote']) > 500:
            errors['quote'] = "Quote must be greater than 10 characters and less than 500 characters."
        return errors


class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    user = models.ForeignKey(login_models.User, related_name="quotes", on_delete = models.CASCADE)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Like(models.Model):
    liked_quote = models.ForeignKey(Quote, related_name="likes", on_delete = models.CASCADE)
    liked_by = models.ForeignKey(login_models.User, related_name="likes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
