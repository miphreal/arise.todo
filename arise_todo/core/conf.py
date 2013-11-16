from arise_todo.storage.backends import text_file
STORAGES = {
    'text_file': text_file.Storage,
}

DEFAULT_STORAGE = {
    'name': 'text_file',
    'options': {'file': '~/.config/arise.todo/todo'}
}
