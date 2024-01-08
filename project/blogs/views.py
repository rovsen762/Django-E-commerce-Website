from django.shortcuts import render
from .models import Blog, Category
from django.views.generic import ListView
# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def blog_detail(request, category_slug , blog_id):
    blog = Blog.objects.get(category__slug=category_slug, id=blog_id)
    blog_recent = Blog.objects.all().order_by('-date')[:5]
    categories = Category.objects.all()
    context = {
        'blog': blog,
        'categories': categories,
        'blog_recent': blog_recent
    }
    return render(request, 'blog_detail.html', context)

def category_list(request, category_slug):
    blogs = Blog.objects.all().filter(category__slug = category_slug)
    categories = Category.objects.all()
    context = {
        
        'blogs': blogs,
        'categories': categories
    }
    return render(request, 'blogs.html', context)

def search(request):
    blogs = Blog.objects.filter(name__contains = request.GET['search'])
    categories = Category.objects.all()
    context = {
        'blogs': blogs,
        'categories': categories
    }
    return render(request, 'blogs.html', context)
