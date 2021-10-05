from django import forms

class CreateListingForm(forms.Form):
    auction = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Title'
            }
        )
    )
    note = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Description',
            'rows': '3'
            }
        )
    )
    est_retail = forms.FloatField(
        label='',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Est. Retail Value',
            'min': '0',
            'step': 'any'
            }
        )
    )
    initial_bid = forms.FloatField(
        label='',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Initial bid',
            'min': '0',
            'step': 'any'
            }
        )
    )
    category = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Category'
            }
        )
    )
    thumbnail = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Thumbnail'
            }
        )
    )

    def clean_initial_bid(self):
        value = self.cleaned_data.get('initial_bid')
        if isinstance(value, float) and value > 0:
            return value
        raise forms.ValidationError('should be a number > 0')

    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category.lower()

class CreateCommentForm(forms.Form):
    comment = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control-md lead form-group',
            'rows': '3',
            'cols': '100'
            }
        )
    )

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) > 0 and len(comment) <= 254:
            return comment
        return self.errors
