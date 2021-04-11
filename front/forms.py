from django import forms


class AttemptForm(forms.Form):
    file = forms.FileField(label='Файл решения',
                           help_text='Не забудьте проверить систему координат и наличие нужного '
                                     'столбца в таблице атрибутов!')
