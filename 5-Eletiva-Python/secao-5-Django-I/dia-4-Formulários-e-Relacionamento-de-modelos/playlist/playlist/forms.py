from django import forms
from playlist.validators import validate_music_length, validate_name_is_char


class CreateMusicForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        validators=[validate_name_is_char],
        label="Nome da música",
    )
    recorded_at = forms.DateField(
        label="Data de gravação",
        widget=forms.DateInput(attrs={"type": "date"}),
        initial="2023-07-06",
    )
    length_in_seconds = forms.IntegerField(
        validators=[validate_music_length],
        label="Duração em segundos",
        help_text="Insira a quantidade de segundos"
    )


class CreatePlaylistForm(forms.Form):
    name = forms.CharField(max_length=50)
    is_active = forms.BooleanField()


class CreateSingerForm(forms.Form):
    name = forms.CharField(max_length=50, validators=[validate_name_is_char])
