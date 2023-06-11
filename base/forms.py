from typing import Any, Mapping, Optional, Type, Union
from django import forms
from datetime import datetime

from phonenumber_field.formfields import PhoneNumberField

from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from .models import Region, Amount


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Отправить сообщение'))


    SUBJECT_CHOICES = [
        ("Сотрудничество", 'Сотрудничество'),
        ("По вопросам рекламы", 'По вопросам рекламы'),
        ("Отзыв", 'Отзыв/Благодарность'),
    ]

    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label="Тема письма", required=True)
    name = forms.CharField(max_length=100, required=True, label="Введите Ваше имя:", 
                           widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    email = forms.EmailField(required=True, label="Ваш email адрес", 
                             widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    phone = PhoneNumberField(label="Введите номер телефона", region="RU")
    message = forms.CharField(max_length=500, required=True, label="Введите сообщение",
                              widget=forms.Textarea(attrs={'autocomplete': 'off'}))
    

class PhotographersForm(forms.Form):

    DURATION_CHOICES = [
        ("1 час", '1 час / 1 500'),
        ("3 часа", '3 часа / 3 000'),
    ]

    PARTICIPANTS_CHOICES = [
        ("4 человека", "4 чел. + 0 доп."),
        ("5 человек", "4 чел. + 1 доп."),
        ("6 человек", "4 чел. + 2 доп."),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Отправить заявку'))

    name = forms.CharField(max_length=50, required=True, label="Ваше имя", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
    surname = forms.CharField(max_length=100, required=True, label="Ваша фамилия", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
    email = forms.EmailField(required=True, label="Введите Ваш email",
                             widget=forms.EmailInput(attrs={'autocomplete' : 'off'}))
    phone = forms.CharField(max_length=100, required=True, label="Номер телефона", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
    date = forms.DateField(required=True, label="Выберите желаемую дату съемки",
                           widget=forms.DateInput(attrs={'type' : 'date'}))
    time = forms.TimeField(required=True, label="Выберите время сеанса",
                           widget=forms.TimeInput(attrs={'type' : 'time', 'max' : datetime.now().time}))
    participants = forms.ChoiceField(choices=PARTICIPANTS_CHOICES, required=True, label="Выберите количество участников",
                                 widget=forms.RadioSelect())
    duration = forms.ChoiceField(choices=DURATION_CHOICES, required=True, label="Продолжительность фотосессии",
                                 widget=forms.RadioSelect())
    

class TreeAdoptionForm(forms.Form):

    TEAMMATES_COUNT_CHOICES = [
        ("2", "2 человека"),
        ("3", "3 человека"),
        ("4", "4 человека"),
        ("5", "5 человек"),
        ("6", "6 человек"),
    ]

    TREES_COUNT_CHOICES = [
        ("1", "1 дерево"),
        ("2", "2 дерева"),
        ("3", "3 дерева"),
        ("4", "4 дерева"),
        ("5", "5 деревьев"),
    ]

    SORTS_CHOICES = [
        ("Рэд Хейвен", "Рэд Хейвен"),
        ("Коллинз", "Коллинз"),
        ("Освежающий", "Освежающий"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Подать заявку на усыновление'))

    team_name = forms.CharField(max_length=50, required=True, label="Название Вашей команды", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
    team_leader = forms.CharField(max_length=50, required=True, label="Руководитель команды", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
    email = forms.EmailField(required=True, label="Введите Ваш email",
                             widget=forms.EmailInput(attrs={'autocomplete' : 'off'}))
    phone = forms.CharField(max_length=100, required=True, label="Номер телефона", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
    team_mates_count = forms.ChoiceField(choices=TEAMMATES_COUNT_CHOICES, required=True, label="Количество человек в команде",
                                 widget=forms.RadioSelect())
    sorts = forms.ChoiceField(choices=SORTS_CHOICES, required=True, label="Выбранные сорта")
    trees_count = forms.ChoiceField(choices=TREES_COUNT_CHOICES, required=True, label="Количество деревьев",
                                 widget=forms.RadioSelect())
    

# форма заказа

class OrderForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Подтвердить заказ'))

        if "region" in self.data:
            region_id = int(self.data.get("region"))
            self.fields["amount"].queryset = Amount.objects.filter(region_id=region_id)

    name = forms.CharField(max_length=50, required=True, label="Имя заказчика/Название организации", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))

    email = forms.EmailField(required=True, label="Введите Ваш email",
                             widget=forms.EmailInput(attrs={'autocomplete' : 'off'}))
    phone = forms.CharField(max_length=100, required=True, label="Номер телефона", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))

    region = forms.ModelChoiceField(queryset = Region.objects.all(), 
                                    label="Выберите регион доставки",
                                    widget = forms.Select(attrs={
                                        "hx-get": "/load_amount/",
                                        "hx-target": "#id_amount",})) 
    address = forms.CharField(max_length=300, required=True, label="Точный адрес доставки", 
                           widget=forms.TextInput(attrs={'autocomplete' : 'off'}))
    
    amount = forms.ModelChoiceField(label="Выберите количество ящиков",
                                    queryset=Amount.objects.none())  
    is_combined = forms.BooleanField(label="Комбинированный заказ")
    

    
