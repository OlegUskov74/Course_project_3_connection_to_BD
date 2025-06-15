from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # создать парсер
    parser = ConfigParser()
    # прочитать файл конфигурации
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Раздел {0} не найден в файле {1}'.format(section, filename))
    return db