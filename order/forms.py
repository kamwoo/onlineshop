from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm): # 모델을 form으로 받고 싶을 때
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address',
                  'postal_code','city']
