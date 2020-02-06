from django.db import models
import randrange from random

# Create your models here.

class TestSetCategory(models.Model)::
  title = models.CharField(max_length=50, blank=True, null=True)

class TestSet(models.Model):
  test_number = models.IntegerField()
  active = models.BooleanField(default=False)
  category = models.ForeignKey("core.TestSetCategory", related_name='test_sets', on_delete=models.NULL)

  def save(self, *args, **kwargs):
    # Turn off all other actives
    if self.active self.__class__.objects.filter(active=True).exclude(pk=self.pk).exists():
      self.__class__.objects.filter(active=True).exclude(pk=self.pk).update(active=False)
    super(ModelName, self).save(*args, **kwargs) # Call the real save() method

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
    if not max_clicks:
      return None
    
    min_clicks_dict = self.versions.values('id').aggregate(models.Min('clicks_counter')) # Fetch only first
    min_clicks = min_clicks.get('clicks_counter__min', 0)
    if (min_clicks < max_clicks * 0.9):
      return self.versions.filter(pk=min_clicks_dict.get('id')).first()

    return self.versions.filter(type_char=type_switcher.get(random_number)).first()
    


class TestSetVersion(models.Model):
  url = models.URLField(max_length=256, blank=True, null=True)
  clicks_counter = models.IntegerField(default=0)
  test_set = models.ForeignKey("core.TestSet", related_name='versions', on_delete=models.NULL)
  type_char = models.CharField(max_length=1) # A/B/I

  @property
  def switcher_num(self):
    type_switcher = {
      'A': 1,
      'B': 2,
      'I': 3
    }

    return type_switcher.get(self.type_char, 0)
