from typing import Protocol
from graph_service import GraphAnalysisResult
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

class OutputHandler(Protocol):
    def handle(self, result: GraphAnalysisResult) -> None: ...

class FileOutputHandler:
    def __init__(self, filename: str = 'result.txt'):
        self.filename = filename
    
    def handle(self, result: GraphAnalysisResult) -> None:
        """Сохраняет результаты в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            self._write_header(f, result)
            self._write_adjacency_matrix(f, result)
            self._write_components_analysis(f, result)
        
        print(f"Результаты сохранены в файл '{self.filename}'")
    
    def _write_header(self, f, result: GraphAnalysisResult):
        f.write("АНАЛИЗ ГРАФА ЭРДЁША-РЕНЬИ\n")
        f.write("=" * 50 + "\n")
        f.write(f"Параметры: n={result.params.n}, p={result.params.p}\n")
        f.write(f"Вершин: {result.total_nodes}, Рёбер: {result.total_edges}\n")
        f.write(f"Компонент связности: {result.total_components}\n\n")
    
    def _write_adjacency_matrix(self, f, result: GraphAnalysisResult):
        """Записывает матрицу смежности"""
        f.write("МАТРИЦА СМЕЖНОСТИ:\n")
        f.write("-" * 50 + "\n")
        
        n = result.total_nodes
        matrix = nx.adjacency_matrix(result.graph).toarray()
        
        if n <= 30:
            # Полная матрица для небольших графов
            for i in range(n):
                for j in range(n):
                    f.write(f"{int(matrix[i, j])} ")
                f.write("\n")
        else:
            # Компактный вид для больших графов
            f.write(f"Размер: {n}×{n}\n")
            f.write(f"Ненулевых элементов: {np.sum(matrix)}\n")
            f.write("Фрагмент 10×10:\n")
            
            for i in range(min(10, n)):
                for j in range(min(10, n)):
                    f.write(f"{int(matrix[i, j])} ")
                f.write("\n")
        f.write("\n")
    
    def _write_components_analysis(self, f, result: GraphAnalysisResult):
        """Записывает анализ компонент связности"""
        f.write("АНАЛИЗ КОМПОНЕНТ СВЯЗНОСТИ:\n")
        f.write("-" * 50 + "\n")
        
        for comp in result.components:
            f.write(f"Компонента {comp.number}:\n")
            f.write(f"  Размер: {comp.size} вершин\n")
            f.write(f"  Связность: {comp.is_connected}\n")
            f.write(f"  Радиус: {comp.radius}\n")
            f.write(f"  Диаметр: {comp.diameter}\n")
            f.write(f"  Плотность: {comp.size / result.total_nodes:.3f}\n\n")

class ConsoleOutputHandler:
    def handle(self, result: GraphAnalysisResult) -> None:
        """Только базовая информация в консоль"""
        print(f"\nГраф: n={result.params.n}, p={result.params.p}")
        print(f"Вершин: {result.total_nodes}, Рёбер: {result.total_edges}")
        print(f"Компонент связности: {result.total_components}")

class VisualizationOutputHandler:
    def handle(self, result: GraphAnalysisResult) -> None:
        """Упрощенная визуализация"""
        try:
            if result.total_nodes > 100:
                print(f"Визуализация пропущена (n={result.total_nodes} > 100)")
                return
            
            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(result.graph, k=0.3, iterations=50)
            
            nx.draw(result.graph, pos,
                   node_color='lightblue', 
                   node_size=200,
                   edge_color='gray',
                   alpha=0.7)
            
            # Только основные параметры на графике
            plt.title(f"Граф Эрдёша-Реньи\np={result.params.p}, компонент: {result.total_components}, вершин: {result.total_nodes}")
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Matplotlib не установлен")

class OutputService:
    def __init__(self, handlers: list[OutputHandler]):
        self.handlers = handlers
    
    def process_result(self, result: GraphAnalysisResult) -> None:
        for handler in self.handlers:
            handler.handle(result)