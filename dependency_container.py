from graph_service import GraphService, GraphParams
from output_service import OutputService, FileOutputHandler, ConsoleOutputHandler, VisualizationOutputHandler
from user_interface import UserInterface

class DIContainer:
    def __init__(self):
        self._services = {}
    
    def register(self, name: str, factory):
        """Регистрирует фабрику сервиса"""
        self._services[name] = factory
    
    def resolve(self, name: str, **kwargs):
        """Создает экземпляр сервиса"""
        if name not in self._services:
            raise ValueError(f"Сервис {name} не зарегистрирован")
        return self._services[name](self, **kwargs)

def configure_container() -> DIContainer:
    """Настраивает DI контейнер"""
    container = DIContainer()
    
    # Регистрируем фабрики сервисов
    container.register('graph_service', lambda c, params: GraphService(params))
    container.register('output_service', lambda c, **kwargs: OutputService([
        FileOutputHandler(),
        ConsoleOutputHandler(),
        VisualizationOutputHandler()
    ]))
    container.register('user_interface', lambda c, **kwargs: UserInterface(
        on_params_received=kwargs['on_params_received']
    ))
    
    return container