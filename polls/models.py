import datetime

from django.db import models
from django.utils import timezone

NAME_CHOICES = (
    ('Jan', 'Jan'),
    ('Sam', 'Sam'),
    ('Radim', 'Radim'),
    ('Stepan', 'Stepan'),
)

class Person(models.Model):
    name = models.CharField(
        max_length=6
        )
    spendings = models.FloatField('spendings', default = 0)

    def __str__(self):
        return self.name

class Thing(models.Model):
    thing_description = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    price = models.FloatField('price')
    found_price = models.FloatField('found_price', null=True)
    buyer = models.ForeignKey(
                Person,
                on_delete=models.SET_NULL,
                null=True
                )
    flag = models.IntegerField('flag', default=3)
    def __str__(self):
        return self.thing_description



''' class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text '''
