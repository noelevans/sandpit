from django.forms                 import ModelForm
from django.forms                 import ValidationError
from django.contrib.admin         import widgets
from django                       import forms
from django.contrib.auth.models   import User
from django.contrib.auth.forms    import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from tridates.events.models       import Event


@csrf_protect
class EventForm(ModelForm):
    
    duration   = forms.IntegerField(label='Is the event over 1 / 2 / 3 days?')
    start_date = forms.DateField(('%d/%m/%Y',),
        label='Event start date',
        widget=forms.widgets.DateInput(format="%d/%m/%Y"))
	
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].initial = "DD/MM/YYYY"
        self.fields['duration'].initial = 1
        #self.fields['numeracy'] = widgets.

    def clean_duration(self):
        data = self.cleaned_data['duration']
        if data < 1 or data > 4:
            raise ValidationError("Enter the amount of days that the event covers")
        return data
    
    def clean_start_date(self):
        print "cc"
        date = self.cleaned_data['start_date']
        print date
        return date

		
    def clean_data(self):
        cleaned_data = self.cleaned_data
        # to avoid entering duplicate events
        start_date = cleaned_data.get('start_date')
        print "gg: " + str(start_date)
        duration = cleaned_data.get('duration')
        region = cleaned_data.get('region')
        if Event.objects.count(start_date=start_date, duration=duration, region__name=region):
            raise ValidationError("Enter the amount of days that " + 
                "the event covers")
        
    class Meta:
        model = Event
        #numeracy = forms.IntegerField(label='Robot test')
        fields = (
            'name', 'start_date', 'duration', 'disciplines',
            'address', 'region', 'website', 'status', 'description',
            #'numeracy',
        )


class UserCreationFormWithEmail(UserCreationForm):

    #next = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(UserCreationFormWithEmail, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        #self.fields['next'].is_hidden = True
        #self.fields['next'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',) 

