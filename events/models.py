from django.db import models


class Event(models.Model):
    eventBanner = models.TextField()
    eventPageURL = models.URLField()
    eventStartDate = models.DateTimeField(null=True, blank=True)
    eventEndDate = models.DateTimeField(null=True, blank=True)
    validStartDate = models.DateTimeField(null=True, blank=True)
    validEndDate = models.DateTimeField(null=True, blank=True)


class formdata(models.Model):
    visitStartDate = models.DateTimeField(null=False)
    visitEndDate = models.DateTimeField(null=False)
    noOfGuestAges_10plus = models.IntegerField(null=False)
    noOfGuestAges_3to9 = models.IntegerField(null=False)
    noOfThemeParkDays = models.IntegerField(null=False)
    floridaResident = models.BooleanField(null=False)
    email = models.EmailField(unique=True, null=False)
