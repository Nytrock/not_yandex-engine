### def correct_text(text: str) -> tuple
Функция, принимающая на вход строку и, в результате обработки с помощью
библиотеки **enchant**, возвращающая исправленную строку и, если исправления
вообще были, текст, в котором при анализе htmlем с помощью специального тэга
выделяются исправленные слова.