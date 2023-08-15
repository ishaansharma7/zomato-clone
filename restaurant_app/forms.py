from django import forms

class DateRangeForm(forms.Form):
    date1 = forms.DateField(label='Start Date ', widget=forms.DateInput(attrs={'type': 'date'}))
    date2 = forms.DateField(label='End Date ', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        date1 = cleaned_data.get('date1')
        date2 = cleaned_data.get('date2')

        if date1 and date2 and date1 >= date2:
            raise forms.ValidationError("End date should be greater than start date.")

        return cleaned_data
