from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from blogs.models import Blog
from store.models import Product



# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all().order_by('-date')[:3]
        context['products'] = Product.objects.all().order_by('-date')[:4]
        return context

class ContactView(SuccessMessageMixin,FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    success_message = 'Your message has been sent successfully'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)