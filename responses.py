def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hi!'

    if 'what is love?' in processed:
        return 'Love is Egorka'
    else:
        return 'Abrakadabra'