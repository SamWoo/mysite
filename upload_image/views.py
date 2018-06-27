from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from upload_image.models import Image


@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        # print(images)
        for image in images:
            new_img = Image(img=image)
            new_img.save()
    # return redirect('upload_image:show')
    return render(request, 'upload_image/uploadimg.html')


@csrf_exempt
def showImage(request):
    images = Image.objects.all()
    context = {
        'images': images,
    }
    # for img in images:
    #     print(img)
    return render(request, 'upload_image/showimg.html', context=context)
