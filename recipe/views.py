from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.files.base import ContentFile
import requests
from .models import Recipe

def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'front.html', {'recipes': recipes})

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-id')
    print('DEBUG: Recipes passed to template:')
    for r in recipes:
        print(f'ID: {r.id}, Name: {r.name}, Description: {r.description}')
    return render(request, 'front.html', {'recipes': recipes})

def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')
        image_url = request.POST.get('image_url')
        
        # Debug information
        print("POST Data received:")
        print(f"Name: {name}")
        print(f"Description: {description}")
        print(f"Image File: {image_file}")
        print(f"Image URL: {image_url}")

        if name and description:
            # Create a recipe instance in memory without saving it yet
            recipe = Recipe(name=name, description=description)

            # Handle image upload from file
            if image_file:
                recipe.image = image_file
            # Handle image upload from URL
            elif image_url:
                try:
                    response = requests.get(image_url, stream=True)
                    if response.status_code == 200:
                        # Get a valid filename from the URL
                        img_name = image_url.split('/')[-1].split('?')[0]
                        # If no extension in filename, try to get it from Content-Type
                        if '.' not in img_name:
                            content_type = response.headers.get('Content-Type', '')
                            if 'image/jpeg' in content_type:
                                img_name += '.jpg'
                            elif 'image/png' in content_type:
                                img_name += '.png'
                            elif 'image/webp' in content_type:
                                img_name += '.webp'
                            else:
                                img_name += '.jpg'  # default to jpg
                        
                        # Save the downloaded content to the image field
                        recipe.image.save(img_name, ContentFile(response.content), save=False)
                except (requests.exceptions.RequestException, ValueError) as e:
                    print(f"Error downloading image from URL: {e}")
            
            # Now, save the recipe instance to the database once.
            # This will save the recipe and the image (if any) correctly.
            recipe.save()
            
            # Debug information after save
            print("\nRecipe saved:")
            print(f"Recipe ID: {recipe.id}")
            print(f"Image name: {recipe.image.name if recipe.image else 'No image'}")
            print(f"Image URL: {recipe.image.url if recipe.image else 'No image'}")
            print(f"Image path: {recipe.image.path if recipe.image else 'No image'}")
            
            # Redirect to the browse page to see the newly added recipe
            return redirect('browse_recipes')

    return render(request, 'add_recipe.html')

def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'view_recipe.html', {'recipe': recipe})

def browse_recipes(request):
    query = request.GET.get('q', '')
    if query:
        recipes = Recipe.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by('-id')
    else:
        # Show all recipes, ordered by the most recently created
        recipes = Recipe.objects.all().order_by('-id')
    
    # Add debug information
    for recipe in recipes:
        print(f"Recipe: {recipe.name}")
        print(f"Image URL: {recipe.image.url if recipe.image else 'No image'}")
        print(f"Image path: {recipe.image.path if recipe.image else 'No image'}")
        
    return render(request, 'browse_recipes.html', {'recipes': recipes})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')