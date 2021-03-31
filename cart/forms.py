from django import forms

# 클라이언트 화면에 입력 폼을 만들어준다.
# 사용자가 입력한 데이터에 대한 전처리

class AddProductForm(forms.Form):
    quantity= forms.IntegerField()
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    # boolean은 기본으로 false로 설정해줘야한다. 클라이언트에 보여줄 필요가 없기 때문에 widget은 히든으로 한다.


