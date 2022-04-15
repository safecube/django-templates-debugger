# Django Templates Debugger

## Usage

### settings.py

.. code-block:: python

	INSTALLED_APPS += [
		"templates_debugger"
	]

### urls.py

.. code-block:: python

	if settings.DEBUG:
		urlpatterns += path("templates/", include("templates_debugger.urls"))


### Templates

.. code-block::

	{% load templates_debugger %}
	{%  debug_var_faker 'name' 'first_name' %}
