def get_error_message(response):
    if response.text:
        message = \
            "Server response: {}, {} " \
            .format(response.status_code, response.text)
    else:
        message = \
            "Server response: {}" \
            .format(response.status_code)

    if response.status_code == 404:
        message = "Resource not found. {}".format(message)

    return message
