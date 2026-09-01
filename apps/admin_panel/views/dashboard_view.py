from django.shortcuts import render

def DashboardView(request):
    return render(request, 'admin_panel/dashboard.html')