from typing import List
import re

import numpy as np
import pandas as pd
import networkx as nx
from scipy.spatial import distance

from latent_semantic_analysis import *
import constants
from typing import List, Dict, Any, Optional

class RouteRecommender:
    def __init__(self, G: nx.MultiDiGraph, lsa: LSA):
        self.G = G
        self.lsa = lsa
        self.all_node_types = ['Flight', 'airlines', 'Route']
        self.target_node = None

    def _add_Flight_node(self, data: Dict[str, Any]) -> None:
        node_name = f"Flight-{self.G.graph['num_Flights']}"
        processed_Flight_details = self.lsa.preprocess_text(data['Flight_details'])
        vectorized_Flight_details = self.lsa.vectorize(processed_Flight_details)

        self.G.add_node(node_name, node_type='Flight', 
                        reduced_tfidf=vectorized_Flight_details, **data)
        self.G.graph['num_Flights'] += 1
        self.target_node = node_name

        for n in self.G:
            if self.G.nodes[n]['node_type'] == 'Route':
                continue
            elif self.G.nodes[n]['node_type'] == 'Flight':
                this_node_expertise = self.G.nodes[n]['expertise']
                if this_node_expertise == data['expertise']:
                    self.G.add_edge(node_name, n, edge_type='expertise_match',
                                    weight=constants.EXPERTISE_MATCH_WEIGHT)
                    self.G.add_edge(n, node_name, edge_type='expertise_match',
                                    weight=constants.EXPERTISE_MATCH_WEIGHT)
       
    def _add_airlines_node(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError()  

    def _add_Route_node(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError()  

    def add_node_to_graph(self, node_type: str, node_data: Dict[str, Any]) -> None:
        if node_type not in self.all_node_types:
            raise ValueError(f'Node type must be one of {self.all_node_types}, received {node_type} instead.')

        if node_type == 'Flight':
            self._add_Flight_node(node_data)
        elif node_type == 'airlines':
            self._add_airlines_node(node_data)
        elif node_type == 'Route':
            self._add_Route_node(node_data)

    def rank_nodes(self, personalized: bool = False, target_node: Optional[str] = None,
                   return_node_type: Optional[str] = 'Route', alpha: float = 0.5) -> Dict[str, float]:
        if personalized:
            ranks = nx.pagerank(self.G, alpha, personalization={target_node: 1})
        else:
            ranks = nx.pagerank(self.G, alpha)

        filtered_ranks = {key: value for key, value in ranks.items() if key.startswith(return_node_type)}
        sorted_ranks = dict(sorted(filtered_ranks.items(), key=lambda x: x[1], reverse=True))
        return sorted_ranks

    def search(self, keywords: str) -> List[str]:
        results = []
        processed_keywords = set(keywords.lower().translate(str.maketrans('', '', string.punctuation)).split())

        for n in self.G:
            if self.G.nodes[n]['node_type'] == 'Flight':
                continue
            elif self.G.nodes[n]['node_type'] in ['Route', 'airlines']:
                node_keywords = set(self.G.nodes[n]['keywords'])
                if processed_keywords.issubset(node_keywords):
                    results.append(n)

        return results

    def _rank_node_with_context(self, target_node: str, context_nodes: List[str],
                                alpha: float, return_node_type: Optional[str] = 'Route') -> Dict[str, float]:
        personalized = {target_node: 1}
        personalized.update({node: 1 for node in context_nodes})
        ranks = nx.pagerank(self.G, alpha, personalization=personalized)

        filtered_ranks = {key: value for key, value in ranks.items() if key.startswith(return_node_type)}
        sorted_ranks = dict(sorted(filtered_ranks.items(), key=lambda x: x[1], reverse=True))
        return sorted_ranks
