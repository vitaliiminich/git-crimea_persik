from django.contrib import admin

# Register your models here.

from .models import Month, Sort, Faq, Article, Agreement, Region, Amount

admin.site.register(Month)
admin.site.register(Sort)
admin.site.register(Faq)
admin.site.register(Article)
admin.site.register(Agreement)
admin.site.register(Region)
admin.site.register(Amount)

