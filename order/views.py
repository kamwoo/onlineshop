from django.shortcuts import render, get_object_or_404
from .models import *
from cart.cart import Cart
from .forms import *

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # 입력받은 정보를 후처리
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # form이 정상이면
            order = form.save()
            if cart.coupon:
                order.coupon = cart.coupon
                # order.discount = cart.coupon.amount
                order.discount = cart.get_discount_total()
                order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price = item['price'],quantity=item['quantity'])
            cart.clear()

            return render(request, 'order/created.html',{'order':order})
    else:
        # 주문자 정보를 입력받는 페이지
        form = OrderCreateForm()

    return render(request, 'order/create.html', {'cart': cart, 'form':form})


# 자바스크립트가 동작하지 않는 환경에서도 주문은 가능해야한다.
def order_complete(request): # 주문 정보를 받고 완료하는 페이지, 완료기능은 없다.
    order_id = request.GET.get('order_id')
    # order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/created.html',{'order':order})


from django.views.generic.base import View
from django.http import JsonResponse

# dispatch : http method에 따라서 분기를 해준다.
# 함수형 뷰에서는 request가 post인지 get인지를 if로 걸러서 사용했지만, class형에서는 dispatch가 분기를 해준다
class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인하지 않았을 때
            return JsonResponse({"authenticated":False},status=403)

        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # form이 정상이면
            order = form.save(commit=False) # 데이터베이스에 query가 두번 날라가지 않게 한다.
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.get_discount_total()
            order.save() # db에 한번 날라간다.

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            data = {
                "order_id": order.id
            }
            return JsonResponse(data)

        else:
            return JsonResponse({}, status=401)

class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인하지 않았을 때
            return JsonResponse({"authenticated":False},status=403)

        order_id = request.POST.get('order_id')
        order= Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(order=order, amount=amount)

        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id" : merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderImpAjaxView(View):
    # 제대로 결제금액으로 되있는지 확인하는 과정
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인하지 않았을 때
            return JsonResponse({"authenticated":False},status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(order=order, merchant_order_id=merchant_id, amount=amount)
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id # 제대로 정보가 있다면 이것으로 업데이트한다.
            # trans.success = True
            trans.save()
            order.paid = True
            order.save()

            data = {
                "works":True
            }
            return JsonResponse(data)
        else:
            return JsonResponse({},status=401)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/admin/detail.html', {'order':order})

# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import weasyprint

# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('order/admin/pdf.html', {'order':order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0]+'/css/pdf.css')])
#     return response