from django              import forms
from django.forms.models import ModelForm

from models                        import Profile
from arts_meetup.tags.models       import *
from arts_meetup.consts.uk_places  import UK_PLACES

GENDERS = (('N', ''), ('M', 'Male'), ('F', 'Female'))
TAGS    = (('R', 'Role'), ('I', 'Interests'))

class UserSearchForm(ModelForm):

    class Meta:
        model  = Profile
        fields = ('sex', 'city', 'role', 'next_free_from', 'next_free_until')


class AddRoleForm(forms.Form):

    new_roles = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="")

    def __init__(self, request, *args, **kwargs):
        super(AddRoleForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        if Profile.VENUE == up.type:
            not_roles = VenueTag.objects.exclude(profile=up)
        elif Profile.GROUP == up.type:
            not_roles = GroupTag.objects.exclude(profile=up)
        else:
            not_roles = RoleTag.objects.exclude(profile=up)
        self.fields['new_roles'].choices = [
            (r.name, r.name) for r in not_roles]



class RemoveRoleForm(forms.Form):

    to_go_roles = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="")

    def __init__(self, request, *args, **kwargs):
        super(RemoveRoleForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        if Profile.VENUE == up.type:
            up_roles = up.venue_tags.all()
        elif Profile.GROUP == up.type:
            up_roles = up.group_tags.all()
        else:
            up_roles = up.role.all()
        self.fields['to_go_roles'].choices = [
            (r.name, r.name) for r in up_roles]



class AddFriendsForm(forms.Form):

    new_friends = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="")

    def __init__(self, request, *args, **kwargs):
        super(AddFriendsForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        not_friends = Profile.objects.exclude(user=up)
        self.fields['new_friends'].choices = [
            (f.id, f._get_full_name()) for f in not_friends]




class RemoveFriendsForm(forms.Form):

    to_go_friends = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="")

    def __init__(self, request, *args, **kwargs):
        super(RemoveFriendsForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        up_friends = up.friends.all()
        self.fields['to_go_friends'].choices = [
            (f.id, f.name) for f in up_friends]




class AddInterestsForm(forms.Form):

    new_interests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="")

    def __init__(self, request, *args, **kwargs):
        super(AddInterestsForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        not_interests = OtherTag.objects.exclude(userprofile=up)
        self.fields['new_interests'].choices = [
            (i.name, i.name) for i in not_interests]


class RemoveInterestsForm(forms.Form):

    to_go_interests = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="")

    def __init__(self, request, *args, **kwargs):
        super(RemoveInterestsForm, self).__init__(*args, **kwargs)
        up = request.user.get_profile()
        up_interests = up.other_tags.all()
        self.fields['to_go_interests'].choices = [
            (i.name, i.name) for i in up_interests]


class AddUserLinkForm(forms.Form):

    label = forms.CharField(max_length=64)
    link  = forms.CharField(max_length=128)
    
    