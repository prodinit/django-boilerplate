from users.models import User

def main(email):
    user = User.objects.get(email=email)
    user.delete()
