from django.shortcuts import render
from core.models import TestSet
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def get_active_version(request):
  try:
    test_set = TestSet.get_active_test_set()
    test_set_version = test_set.get_test_version()
    test_set_version.increase_click()
    if test_set_version.redirect:
      return HttpResponseRedirect(redirect_to=test_set_version.url)
    ret = {
      'success': 1,
      'active_app': test_set.campaign.title,
      'active_test_set': test_set.test_number,
      'test_set_version': test_set_version.type_char
    }
  except Exception as e:
    ret = {
      'success': 0,
      'error': e
    }
    print(e)

  return JsonResponse(ret)