from django.shortcuts import render_to_response


def tinymce(request):
    return render_to_response('tinymce.html')
