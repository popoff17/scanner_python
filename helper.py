import importlib

class Helper:
    pass  # Пока что пустой класс

# Логика для добавления методов после определения класса
modules = [
    'helpers.helper_main',
    'helpers.helper_parser',
]

for module in modules:
    #print(f"Importing module: {module}")
    try:
        module_class = importlib.import_module(module)
        #print(f"Successfully imported module: {module}")
    except ImportError as e:
        #print(f"Failed to import module {module}: {e}")
        continue  # Пропускаем модуль, если не удается импортировать

    for attr_name in dir(module_class):
        if not attr_name.startswith('__'):
            #print(f"Found attribute: {attr_name}")
            class_obj = getattr(module_class, attr_name)
            if isinstance(class_obj, type):
                #print(f"Found class: {class_obj.__name__}")

                # Сохраняем статические методы на уровне класса Helper
                for method_name in dir(class_obj):
                    if not method_name.startswith('__'):
                        method = getattr(class_obj, method_name)
                        if callable(method):  # Проверяем, что это метод
                            #print(f"Adding static method: {method_name} from class: {class_obj.__name__}")
                            setattr(Helper, method_name, staticmethod(method))
                        #else:
                            #print(f"{method_name} is not callable.")
            #else:
                #print(f"{attr_name} is not a class.")
