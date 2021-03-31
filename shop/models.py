from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    # category 이름이나 제품이름으로 접근하는 것을 slug로 접근한다고 한다.

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.names

    def get_absolute_url(self): # 상세페이지 결정
        return reverse('shop:product_in_category', args=[self.slug])

# mata_description은 검색엔진에 노출되기위해 만들어준다.
# slug는 제품에 pk대신에 접근하기 위해 사용
# all_unicode를 사용해야 한글을 쓸 수 있다.

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    # models.SET_NULL은 카테고리가 지워져도 상품은 지워지지 않는다. related_name은 카테고리에서 어떤 이름으로 불러올지 결정
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode = True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True) # 상세페이지에 노출되는 설명
    meta_description = models.TextField(blank=True) # 검색엔진에 노출될 설명
    price = models.DecimalField(max_digits=10, decimal_places=2) # 총 10자리의 소수점 2자리까지의 금액을 적을 수 있다.
    stock = models.PositiveIntegerField()
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta: # Meta의 뜻은 다양한 정보를 담있다는 뜻
        # model안에 Meta 클래스는 검색옵션이나 디스플레이된 이름등이 담긴다.
        ordering = ['-created', '-updated']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

