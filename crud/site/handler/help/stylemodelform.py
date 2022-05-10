from django import forms


class StyleModelForm(forms.ModelForm):
    """
    set up the style of the data displaying
    """

    def __init__(self, *args, **kwargs):
        super(StyleModelForm, self).__init__(*args, **kwargs)
        # add styles to ModelForm generated fields
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
