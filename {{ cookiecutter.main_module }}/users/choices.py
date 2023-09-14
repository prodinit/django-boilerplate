import pycountry

COUNTRIES = [country.alpha_2 for country in list(pycountry.countries)]
COUNTRY_CHOICES = tuple(zip(COUNTRIES, COUNTRIES))

MALE = "MALE"
FEMALE = "FEMALE"
PREFER_NOT_TO_RESPOND = "PREFER_NOT_TO_RESPOND"
GENDER_CHOICES = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (PREFER_NOT_TO_RESPOND, "Prefer not to respond"),
)