from django.db.models import Q
def browse_recipes(request):
    query = request.GET.get('q', '')
    if query:
        recipes = Recipe.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        recipes = Recipe.objects.all()
    return render(request, 'browse_recipes.html', {'recipes': recipes})

from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Recipe
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request=request, template_name='front.html')

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'front.html', {'recipes': recipes})

def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        image_url = request.POST.get('image_url')
        recipe = None
        if name and description:
            if image:
                recipe = Recipe(name=name, description=description, image=image)
            elif image_url:
                from django.core.files.base import ContentFile
                import requests
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        img_name = image_url.split('/')[-1]
                        recipe = Recipe(name=name, description=description)
                        recipe.image.save(img_name, ContentFile(response.content), save=False)
                except Exception:
                    pass
            if recipe:
                recipe.save()
                return redirect('browse_recipes')
    return render(request, 'add_recipe.html')