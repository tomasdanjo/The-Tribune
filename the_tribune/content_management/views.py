from django.shortcuts import render

# Create your views here.
def writer_dashboard_view(request):
    user = request.user

    return render(request,'writer_dashboard.html',{'user':user})

# def editor_dashboard_view(request):
#     pass