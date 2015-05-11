import re
from datetime                      import date
from django                        import forms
from django.contrib.auth.models    import User
from django.contrib.admin          import widgets

from arts_meetup.tags.models       import RoleTag
from arts_meetup.users.models      import Profile
from arts_meetup.consts.uk_places  import UK_PLACES



class IndividualRegistrationForm(forms.Form):

#    acc_type   = forms.ChoiceField(choices=Profile.PROFILE_TYPES)

    username          = forms.CharField(max_length=32)
    email             = forms.EmailField()
    city              = forms.ChoiceField(choices=UK_PLACES)
    password1         = forms.CharField(
                            widget=forms.PasswordInput(),
                            max_length=32)
    password2         = forms.CharField(
                            widget=forms.PasswordInput(),
                            max_length=32)
    email_news        = forms.BooleanField(required=False) # contact me about news
    tandcs            = forms.BooleanField()               # contact me about news

    # For Person
    first_name        = forms.CharField(max_length=64)
    last_name         = forms.CharField(max_length=64)
    sex               = forms.ChoiceField(
                            choices=Profile.GENDERS,
                            required=False)
    dob               = forms.CharField(
                            max_length=10,
                            #widget=forms.TextInput(),
                            required=False)
    # picture           = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(IndividualRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget = widgets.AdminDateWidget()
        self.fields['dob'].initial = "DD/MM/YYYY"

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if not re.match("^[A-Za-z0-9_-]*$", username):
            raise forms.ValidationError(
                "Username must have no spaces or special characters")
        elif User.objects.filter(username=username).count() > 0:
            print "===== " + username + " ====="
            raise forms.ValidationError(
                "This username has already been taken. Please choose another")
        return username

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2', '')
        password1 = self.cleaned_data.get('password1', '')
        if password1 != password2:
            raise forms.ValidationError(
                "The passwords entered do not match")
        return password2

    def clean_tandcs(self):
        tandcs = self.cleaned_data.get('tandcs', '')
        if not tandcs:
            raise forms.ValidationError(
                "You must agree to the terms and conditions to use the site")
        return tandcs

    def clean_dob(self):
        err = "Please enter your date of birth in format DD/MM/YYYY eg 22/12/1980"
        dob = self.cleaned_data.get('dob', '')
        print "===" + dob + "==="
        if dob != 'DD/MM/YYYY' and dob != '':
            try:
                splits = dob.split('/')
                dob = date(int(splits[2]), int(splits[1]), int(splits[0]))
            except:
                raise forms.ValidationError(err)
            if not dob:
                raise forms.ValidationError(err)
        return str(dob)



class VenueRegistrationForm(forms.Form):

    name              = forms.CharField(max_length=128)
    username          = forms.CharField(max_length=32)
    email             = forms.EmailField()
    city              = forms.ChoiceField(choices=UK_PLACES)
    password1         = forms.CharField(
                            widget=forms.PasswordInput(),
                            max_length=32)
    password2         = forms.CharField(
                            widget=forms.PasswordInput(),
                            max_length=32)
    email_news        = forms.BooleanField(required=False)  # contact me about news
    tandcs            = forms.BooleanField()                # just to check I ain't suin'

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if not re.match("^[A-Za-z0-9_-]*$", username):
            raise forms.ValidationError(
                "Username must have no spaces or special characters")
        elif User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(
                "This username has already been taken. Please choose another")
        return username

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2', '')
        password1 = self.cleaned_data.get('password1', '')
        if password1 != password2:
            raise forms.ValidationError(
                "The passwords entered do not match")
        return password2

    def clean_tandcs(self):
        tandcs = self.cleaned_data.get('tandcs', '')
        if not tandcs:
            raise forms.ValidationError(
                "You must agree to the terms and conditions to use the site")
        return tandcs


class GroupRegistrationForm(forms.Form):

    name              = forms.CharField(max_length=128)
    username          = forms.CharField(max_length=32)
    email             = forms.EmailField()
    city              = forms.ChoiceField(choices=UK_PLACES)
    password1         = forms.CharField(
                            widget=forms.PasswordInput(),
                            max_length=32)
    password2         = forms.CharField(
                            widget=forms.PasswordInput(),
                            max_length=32)
    email_news        = forms.BooleanField(required=False)  # contact me about news
    tandcs            = forms.BooleanField()                # just to check I ain't suin'

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if not re.match("^[A-Za-z0-9_-]*$", username):
            raise forms.ValidationError(
                "Username must have no spaces or special characters")
        elif User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(
                "This username has already been taken. Please choose another")
        return username

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2', '')
        password1 = self.cleaned_data.get('password1', '')
        if password1 != password2:
            raise forms.ValidationError(
                "The passwords entered do not match")
        return password2

    def clean_tandcs(self):
        tandcs = self.cleaned_data.get('tandcs', '')
        if not tandcs:
            raise forms.ValidationError(
                "You must agree to the terms and conditions to use the site")
        return tandcs


class LoginForm(forms.Form):

    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())


class ChangePasswordForm(forms.Form):

    old_password  = forms.CharField(widget=forms.PasswordInput())
    new_password1 = forms.CharField(
            widget=forms.PasswordInput(),
            label='new password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(),
            label='new password (again)')


class FullSearchForm(forms.Form):

    tag                       = forms.ChoiceField()
    where                     = forms.ChoiceField(choices=UK_PLACES)
    start                     = forms.DateField(label='From')
    until                     = forms.DateField()
    start.is_hidden           = True
    until.is_hidden           = True
    home=""

    def __init__(self, request, *args, **kwargs):
        super(FullSearchForm, self).__init__(*args, **kwargs)
        self.fields['tag'].choices = [
            (r.name, r.name) for r in RoleTag.objects.all()]
        self.fields['start' ].initial = request.GET.get('start', 'DD/MM/YYYY')
        self.fields['until'].initial  = request.GET.get('until', 'DD/MM/YYYY')
        self.fields['tag'].initial    = request.GET.get('tag',   '')
        if request.GET.get('where', ''):
            self.fields['where'].initial = request.GET.get('where', '')
        elif request.user.is_authenticated():
            self.fields['where'].initial = request.user.get_profile().city


class PersonSettingsForm(forms.Form):

    first_name  = forms.CharField(max_length=64)
    last_name   = forms.CharField(max_length=64)
    email       = forms.EmailField()
    sex         = forms.ChoiceField(choices=Profile.GENDERS)
    city        = forms.ChoiceField(choices=UK_PLACES)
    email_news  = forms.BooleanField(
            required=False,
            label="Email me occassionally when ArtsTent is improved")
    email_msged = forms.BooleanField(
            required=False,
            label="Email me when someone contacts me on ArtsTent")

    def __init__(self, request, *args, **kwargs):
        super(PersonSettingsForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        self.fields['first_name'].initial = up.first_name
        self.fields['last_name'].initial = up.last_name
        self.fields['email'].initial = up.user.email
        self.fields['sex'].initial = up.sex
#        self.fields['dob'].initial = up.dob
        self.fields['city'].initial = up.city
        self.fields['email_news'].initial = up.email_news
        self.fields['email_msged'].initial = up.email_msged

class GroupSettingsForm(forms.Form):

    org_name         = forms.CharField(max_length=128)
    email            = forms.EmailField()
    # address_line_1   = forms.CharField(max_length=128, required=False)
    # address_line_2   = forms.CharField(max_length=128, required=False)
    # postcode         = forms.CharField(max_length=10, required=False)
    # telephone        = forms.CharField(max_length=32, required=False)
    city             = forms.ChoiceField(choices=UK_PLACES)
    email_news  = forms.BooleanField(
            required=False,
            label="Email me occassionally when ArtsTent is improved")
    email_msged = forms.BooleanField(
            required=False,
            label="Email me when someone contacts me on ArtsTent")

    def __init__(self, request, *args, **kwargs):
        super(GroupSettingsForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        self.fields['org_name'].initial = up.org_name
        # self.fields['address_line_1'].initial = up.address_line_1
        # self.fields['address_line_2'].initial = up.address_line_2
        # self.fields['postcode'].initial = up.postcode
        # self.fields['telephone'].initial = up.telephone
        self.fields['email'].initial = up.user.email
        self.fields['city'].initial = up.city
        self.fields['email_news'].initial = up.email_news
        self.fields['email_msged'].initial = up.email_msged


class VenueSettingsForm(forms.Form):

    org_name         = forms.CharField(max_length=128)
    email            = forms.EmailField()
    address_line_1   = forms.CharField(max_length=128, required=False)
    address_line_2   = forms.CharField(max_length=128, required=False)
    postcode         = forms.CharField(max_length=10, required=False)
    telephone        = forms.CharField(max_length=32, required=False)
    city             = forms.ChoiceField(choices=UK_PLACES)
    email_news  = forms.BooleanField(
            required=False,
            label="Email me occassionally when ArtsTent is improved")
    email_msged = forms.BooleanField(
            required=False,
            label="Email me when someone contacts me on ArtsTent")

    def __init__(self, request, *args, **kwargs):
        super(VenueSettingsForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        self.fields['org_name'].initial = up.org_name
        self.fields['address_line_1'].initial = up.address_line_1
        self.fields['address_line_2'].initial = up.address_line_2
        self.fields['postcode'].initial = up.postcode
        self.fields['telephone'].initial = up.telephone
        self.fields['email'].initial = up.user.email
        self.fields['city'].initial = up.city
        self.fields['email_news'].initial = up.email_news
        self.fields['email_msged'].initial = up.email_msged



class BioForm(forms.Form):

    bio = forms.CharField(
            max_length=500,
            required=False,
            widget=forms.Textarea
        )

    def __init__(self, request, *args, **kwargs):
        super(BioForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        self.fields['bio'].initial = up.bio.replace('&nbsp;</p><p>', '\n')


class PictureForm(forms.Form):

    picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(PictureForm, self).__init__(*args, **kwargs)
        self.fields['picture'].initial = ""
