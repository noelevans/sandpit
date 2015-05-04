from django              import forms


class MakeTagForm(forms.Form):

    TAGS = (('R', 'Role'),)    # , ('I', 'Interests'))

#    tag_type = forms.ChoiceField(
#        choices=TAGS,
#        widget=forms.RadioSelect,
#        help_text="Role tags are for jobs or positions, Interests... well that's for things you're in to!",
#        required=False)
    tag_name = forms.CharField(
        max_length=32,
        help_text='eg. Neo gothic, Shakespearean, Lighting Director, Props assistant, etc.')
#    description     = forms.CharField(
#        max_length=128,
#        required   =False,
#        help_text  ='(128 characters max)',
#        initial    ='Optional')
    tag_me = forms.BooleanField(
        initial=True,
        label='Tag me with this')

#    def clean_message(self):
#        tag_name = self.cleaned_data['tag_name']
#        num_words = len(tag_name.split())
#        if num_words != 1:
#            raise forms.ValidationError("Tag must be one ")
#        return message
