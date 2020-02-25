from django.db import models
from random import randrange

# Create your models here.

class TestSetCampaign(models.Model):
  title = models.CharField(max_length=50, blank=True, null=True)

class TestSet(models.Model):
  test_number = models.IntegerField()
  active = models.BooleanField(default=False)
  campaign = models.ForeignKey("core.TestSetCampaign", related_name='test_sets', on_delete=models.SET_NULL, blank=True, null=True)

  def save(self, *args, **kwargs):
    # Turn off all other actives
    if self.active and self.__class__.objects.filter(active=True).exclude(pk=self.pk).exists():
      self.__class__.objects.filter(active=True).exclude(pk=self.pk).update(active=False)
    super().save(*args, **kwargs) # Call the real save() method

  @classmethod
  def get_active_test_set(cls):
    return cls.objects.filter(active=True).first()

  def get_test_version(self):
    type_switcher = {
      1: 'A',
      2: 'B',
      3: 'I'
    }
    num_of_versions = self.versions.count()
    if num_of_versions > 0:
      min_range = 1
      max_range = num_of_versions + 1
    else:
      min_range = 0
      max_range = 1
    random_number = randrange(min_range, max_range)
    
    max_clicks = self.versions.aggregate(models.Max('clicks_counter')).get('clicks_counter__max', 0)
    if max_clicks is None:
      return None
    
    min_clicks_dict = self.versions.values('id', 'clicks_counter').order_by('clicks_counter').first() # Fetch only first
    min_clicks = min_clicks_dict.get('clicks_counter', 0)
    if (min_clicks < max_clicks * 0.9):
      return self.versions.filter(pk=min_clicks_dict.get('id')).first()

    return self.versions.filter(type_char=type_switcher.get(random_number)).first()
    


class TestSetVersion(models.Model):
  clicks_counter = models.IntegerField(default=0)
  test_set = models.ForeignKey("core.TestSet", related_name='versions', on_delete=models.SET_NULL, blank=True, null=True)
  type_char = models.CharField(max_length=1) # A/B/I
  url = models.URLField(max_length=256, blank=True, null=True)

  @property
  def switcher_num(self):
    type_switcher = {
      'A': 1,
      'B': 2,
      'I': 3
    }

    return type_switcher.get(self.type_char, 0)

  def increase_click(self):
    self.clicks_counter = self.clicks_counter + 1
    self.save()

  @property
  def redirect(self):
    return self.type_char == 'I'
