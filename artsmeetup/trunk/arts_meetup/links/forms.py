from django                        import forms



class AddUserLinkForm(forms.Form):

    label = forms.CharField(max_length=64)
    link  = forms.CharField(max_length=128)
    
    