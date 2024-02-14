from django import forms

from .models import Game


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


class RequestAcceptForm(forms.Form):
    game_id = forms.IntegerField(widget=forms.HiddenInput)
    request_id = forms.IntegerField(widget=forms.HiddenInput)


class GameUpdateForm(forms.ModelForm):
    template_name = "games/forms/update_form.html"

    class Meta:
        model = Game
        fields = [
            'primary_name',
            'description',
            'description_short',
            'release_year',
            'players_min',
            'players_max',
            'playtime_min',
            'playtime_max',
            'image_url',
            'thumbnail_url',
        ]

        labels = {
            "primary_name": "Name",
        }

        widgets = {
            "primary_name": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            "description": forms.Textarea(attrs={"class": "form-control", "type": "text"}),
            "description_short": forms.Textarea(attrs={"class": "form-control", "type": "text", "rows": 2}),
            "release_year": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "players_min": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "players_max": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "playtime_min": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "playtime_max": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "type": "url"}),
            "thumbnail_url": forms.URLInput(attrs={"class": "form-control", "type": "url"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        players_min = cleaned_data.get("players_min")
        players_max = cleaned_data.get("players_max")
        playtime_min = cleaned_data.get("playtime_min")
        playtime_max = cleaned_data.get("playtime_max")

        if players_min > players_max:
            raise forms.ValidationError(
                "Minimum amount of players must be less than or equal to maximum amount."
            )

        if playtime_min > playtime_max:
            raise forms.ValidationError(
                "Minimum amount of playtime must be less than or equal to maximum amount."
            )

        return cleaned_data
