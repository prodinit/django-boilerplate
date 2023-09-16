{% extends "mail_templated/base.tpl" %}

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
<a href="{{ domain }}api/activate?token={{ token }}">Confirm Email</a>
</p>
<p>Thanks!</p>
{% endblock html %}