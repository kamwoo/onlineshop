import csv

from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse
import datetime

# Register your models here.

def export_to_csv(modeladmin, request, queryset):
    # modeladmin: 어떤것을 선택했는지, request: 요청이 들어오는것, queryset: 어떤 것이 선택됬는지
    opts = modeladmin.model._meta # 필드들의 정보를 얻어온다.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name)

    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")

            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

from django.urls import reverse
from django.utils.safestring import mark_safe

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    html = mark_safe(f"<a href='{url}'>Detail</a>")
    return html

order_detail.short_description = 'Detail'

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    html = mark_safe(f"<a href='{url}'>PDF</a>")
    return html

order_pdf.short_description = 'PDF'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','postal_code','city','paid',order_detail,order_pdf,'created','updated']
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline]
    # order모델과 Foreign key로 엮어져있는 것들을 order를 등록할때 밑에서 같이 별도로 등록하는것
    actions = [export_to_csv]
    # 선택한 것들을 엑셀로 뽑아준다.

admin.site.register(Order, OrderAdmin)