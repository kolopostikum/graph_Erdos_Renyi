from dependency_container import configure_container
from graph_service import GraphParams

class Application:
    def __init__(self):
        self.container = configure_container()
        self.graph_service = None
        self.output_service = self.container.resolve('output_service')
        
        # Создаем UI с колбэком
        self.ui = self.container.resolve(
            'user_interface', 
            on_params_received=self._on_params_received
        )
    
    def _on_params_received(self, params: GraphParams) -> None:
        """Колбэк, вызываемый когда пользователь ввел параметры"""
        # Создаем сервис графа с полученными параметрами
        self.graph_service = self.container.resolve('graph_service', params=params)
        
        # Выполняем анализ
        result = self.graph_service.analyze_components()
        
        # Передаем результат в output service
        self.output_service.process_result(result)
    
    def run(self) -> None:
        """Запускает приложение"""
        self.ui.run()

if __name__ == "__main__":
    app = Application()
    app.run()
    