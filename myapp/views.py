from django.shortcuts import render

def handler_page(request,exception):
    return render(request,'404.html',status=404)