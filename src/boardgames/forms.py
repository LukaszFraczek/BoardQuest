from django import forms


class GameRequestForm(forms.Form):
    bgg_id = forms.CharField(widget=forms.HiddenInput)
    thumbnail_url = forms.URLField(widget=forms.HiddenInput, required=False)
    image_url = forms.URLField(widget=forms.HiddenInput, required=False)
    primary_name = forms.CharField(widget=forms.HiddenInput)
    release_year = forms.CharField(widget=forms.HiddenInput, required=False)
    description = forms.CharField(widget=forms.HiddenInput)
    players_min = forms.CharField(widget=forms.HiddenInput)
    players_max = forms.CharField(widget=forms.HiddenInput)
    playtime_min = forms.CharField(widget=forms.HiddenInput)
    playtime_max = forms.CharField(widget=forms.HiddenInput)
