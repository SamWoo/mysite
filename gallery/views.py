from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from gallery.models import Image


@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        # images = request.FILES.getlist('images')
        images = request.FILES.getlist('files[]')  # ssi-uploader插件返回的数据Key=files[]
        print(images)
        for image in images:
            new_img = Image(img=image)
            new_img.save()
        return HttpResponse("1")
    else:
        return render(request, 'gallery/upload.html')


@csrf_exempt
def showImage(request):
    images = Image.objects.all()
    context = {
        'images': images,
    }
    for img in images:
        print(img)
    return render(request, 'gallery/showimg.html', context=context)
