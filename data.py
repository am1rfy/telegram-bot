# API
URL = 'https://www.1secmail.com/api/v1/'

# параметры передаваемые для генерации рандомной почты
generate_params = {
    'action': 'genRandomMailbox'
}

# параметры передаваемые для получения списка сообщений с почты
check_params = {
    'action': 'getMessages',
    'login': '',
    'domain': '',
}

# параметры передаваемые для получения контента из конкретного сообщения по ID
read_params = {
    'action': 'readMessage',
    'login': '',
    'domain': '',
    'id': ''
}
