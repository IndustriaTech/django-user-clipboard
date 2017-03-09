from user_clipboard.utils.ajax import JSONResponse
from .forms import ModelWithFileForm, ModelWithImageForm


def upload_document(request):
    if request.method == 'POST':
        form = ModelWithFileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            instance = form.save()
            return JSONResponse(request, {
                'data': {
                    'pk': instance.pk,
                    'document': instance.document.url,
                },
            })
        else:
            return JSONResponse(request, {'errors': form.errors})
    else:
        return JSONResponse(request, {'error': 'Method not allowed'}, 405)


def upload_image(request):
    if request.method == 'POST':
        form = ModelWithImageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            instance = form.save()
            return JSONResponse(request, {
                'data': {
                    'pk': instance.pk,
                    'image': instance.image.url,
                },
            })
        else:
            return JSONResponse(request, {'errors': form.errors})
    else:
        return JSONResponse(request, {'error': 'Method not allowed'}, 405)
