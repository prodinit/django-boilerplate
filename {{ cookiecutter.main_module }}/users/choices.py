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

EMAIL = "EMAIL"
PHONE_NUMBER = "PHONE_NUMBER"
GOOGLE = "GOOGLE"
GITHUB = "GITHUB"
AUTH_PROVIDER = (
    (EMAIL, "email"),
    (PHONE_NUMBER, "phone_number"),
    (GOOGLE, "google"),
    (GITHUB, "github"),
)
