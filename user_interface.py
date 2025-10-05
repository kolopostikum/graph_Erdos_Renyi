from graph_service import GraphParams
from typing import Callable, Any

class UserInterface:
    def __init__(self, on_params_received: Callable[[GraphParams], Any]):
        self.on_params_received = on_params_received
    
    def get_parameters(self) -> GraphParams:
        """Получает параметры от пользователя"""
        print("=== ПАРАМЕТРЫ ГРАФА ===")
        
        try:
            n = int(input("Введите количество вершин (n) [50]: ") or 50)
            p = float(input("Введите вероятность ребра (p) [0.01]: ") or 0.01)
            
            if n <= 0:
                raise ValueError("Количество вершин должно быть положительным")
            if p < 0 or p > 1:
                raise ValueError("Вероятность должна быть в диапазоне [0, 1]")
            
            params = GraphParams(n, p)
            return params
            
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
            print("Используются значения по умолчанию: n=50, p=0.01")
            return GraphParams()
    
    def run(self) -> None:
        """Запускает интерфейс пользователя"""
        params = self.get_parameters()
        self.on_params_received(params)