{# ======== Subject of email #}
{% block subject %}
Activate your account at {{ cookiecutter.project_name }}
{% endblock %}

{% block html %}
<p>
You're receiving this email because you tried to signup at {{ cookiecutter.project_name }}.
Please use the activation link to verify your email and successfully signup.
</p>

<p>
<a href="activation_url=activation_url">Confirm Email</a>
</p>
<p>Thanks!</p>
{% endblock html %}