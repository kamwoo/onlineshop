from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    # 카테고리를 등록할 때 해당하는 것을 섞어서 자동으로 필드를 만들어 준다. 자바스크립트가 동작하게 한다.

admin.site.register(Category, CategoryAdmin)

@admin.register(Product)
# 어노테이션 기법 : 해당하는 밑에 것을 부르기전에 먼저 실행하겠다. 함수들에서 많이 쓰고, 위처럼 할 수 있고 이렇게도 할 수 있다.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','slug', 'category','price','stock', 'available_display','available_order', 'created','updated']
    list_filter = ['available_display', 'created','updated','category']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock','available_display','available_order']

