{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}


{%- block header -%}
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8" />
<title>{{title}}</title>

</head>
{%- endblock header -%}

{% block body %}
<body>

{% for section in sections %}
    {{ section.name|e }}
    {% for example in section.examples %}
        <li><a href="{{ example.url }}">{{ example.name|e }}</a>
        
        {% for output in example.outputs %}
            <img src="{{ output }}" width="300">
        {% endfor %}
        </li>
    {% endfor %}
    <br>
{% endfor %}

</body>
{%- endblock body %}

{% block footer %}
</html>
{% endblock footer %}
