import networkx as nx
from dataclasses import dataclass
from typing import List

@dataclass
class GraphParams:
    n: int = 50
    p: float = 0.01

@dataclass
class ComponentAnalysis:
    number: int
    is_connected: bool
    radius: int
    diameter: int
    size: int

@dataclass
class GraphAnalysisResult:
    params: GraphParams
    graph: nx.Graph
    components: List[ComponentAnalysis]
    total_nodes: int
    total_edges: int
    total_components: int

class GraphService:
    def __init__(self, params: GraphParams):
        self.params = params
        self.graph = None
    
    def create_graph(self) -> nx.Graph:
        """Создает граф Эрдёша-Реньи"""
        self.graph = nx.erdos_renyi_graph(self.params.n, self.params.p)
        return self.graph
    
    def analyze_components(self) -> GraphAnalysisResult:
        """Анализирует компоненты связности"""
        if self.graph is None:
            self.create_graph()
        
        components = list(nx.connected_components(self.graph))
        component_analyses = []
        
        for i, component in enumerate(components):
            subgraph = self.graph.subgraph(component)
            comp_size = len(component)
            
            if comp_size == 1:
                radius = diameter = 0
                is_connected = True
            else:
                is_connected = nx.is_connected(subgraph)
                radius = nx.radius(subgraph)
                diameter = nx.diameter(subgraph)
            
            component_analyses.append(
                ComponentAnalysis(i + 1, is_connected, radius, diameter, comp_size)
            )
        
        return GraphAnalysisResult(
            params=self.params,
            graph=self.graph,
            components=component_analyses,
            total_nodes=self.graph.number_of_nodes(),
            total_edges=self.graph.number_of_edges(),
            total_components=len(components)
        )