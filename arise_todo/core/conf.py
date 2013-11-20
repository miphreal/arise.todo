from arise_todo.storage.backends import text_file
STORAGES = {
    'text_file': text_file.TextStorage,
}

DEFAULT_STORAGE = {
    'name': 'text_file',
    'options': {'file_name': '~/.config/arise.todo/todo'}
}
