{% extends "mail_templated/base.tpl" %}

{# ======== Subject of email #}
{% block subject %}
Account activation email
{% endblock %}

{% block html %}
<p>
You're receiving this email because you tried to signup.
Please use the activation link to verify your email and successfully signup.
</p>

<p>
<a href="{{ activation_url }}">Confirm Email</a>
</p>
<p>Thanks!</p>
{% endblock html %}