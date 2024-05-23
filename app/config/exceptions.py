from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
	"""
	Overloading the standart exception handler.
	"""

	# If an exception occurs that does not need to be handled manually, it will be handled by the default way."
	response = exception_handler(exc, context)

	handlers = {
		'ValidationError': _handle_generic_error
	}

	# Determining the exception type
	exception_class = exc.__class__.__name__

	if exception_class in handlers:
		# Handling the exception if it is present in handlers dict
		return handlers[exception_class](exc, context, response)

	return response


def _handle_generic_error(exc, context, response):
	"""
	Append the "errors" keys to the response
	"""
	response.data = {
		"errors": response.data
	}

	return response
