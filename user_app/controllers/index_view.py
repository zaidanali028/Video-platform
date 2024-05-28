
from django.http import HttpResponse



def index_page(request):
   
   return HttpResponse('hello world! :)')

def video_page(request):
   
   return HttpResponse('Video Page :)')


def video_detail_page(request):
   
   return HttpResponse('Video Detail Page :)')
