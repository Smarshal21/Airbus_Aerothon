from typing import Dict, List, Tuple, Any
import logging
import os
import pickle
import string
import sys

import numpy as np
import pandas as pd
import networkx as nx

from sklearn import neighbors
from scipy.spatial import distance
import latent_semantic_analysis
import constants

handler = logging.StreamHandler()
formmater = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formmater)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class NetworkBuilder:

    def __init__(self, airliness_data: pd.DataFrame, 
                Routes_data: pd.DataFrame,
                cv_data: pd.DataFrame) -> None:
        
        if isinstance(airliness_data, pd.DataFrame):
            self.airliness_data = self.airliness_dataframe_to_dict(airliness_data)
        elif isinstance(airliness_data, str):
            self.airliness_data = pd.read_csv(airliness_data)
            self.airliness_data = self.airliness_dataframe_to_dict(self.airliness_data)
        else:
            raise ValueError('data should be a dataframe of a path to that dataframe')

        if isinstance(Routes_data, pd.DataFrame):
            self.Routes_data = self.Routes_dataframe_to_dict(Routes_data)
        elif isinstance(Routes_data, str):
            self.Routes_data = pd.read_csv(Routes_data)
            self.Routes_data = self.Routes_dataframe_to_dict(self.Routes_data)
        else:
            raise ValueError('data should be a dataframe of a path to that dataframe')

        if isinstance(cv_data, pd.DataFrame):
            self.cv_data = self.cv_dataframe_to_dict(cv_data)
        elif isinstance(cv_data, str):
            self.cv_data = pd.read_csv(cv_data)
            self.cv_data = self.cv_dataframe_to_dict(self.cv_data)
        else:
            raise ValueError('data should be a dataframe of a path to that dataframe')

        self.G = None
        self.comparer = None

    def airliness_dataframe_to_dict(self, companies_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        airliness_data = {}
        for i, row in companies_df.iterrows():
            airlines_data = {
                'company_name': row['company_name'],
                'average_rating': row['average_rating'],
                'num_review': row['num_review'],
                'city': row['city'],
                'type': row['type'],
                'num_employee': row['num_employee'],
                'country': row['country'],
                'working_day': row['working_day'],
                'OT': row['OT'],
                'overview': row['overview'],
                'expertise': row['expertise'],
                'benefit': row['benefit'],
                'logo_link': row['logo_link']
            }
            airliness_data[row['company_id']] = airlines_data
        return airliness_data

    def Routes_dataframe_to_dict(self, Routes_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        Routes_data = {}
        for i, row in Routes_df.iterrows():
            Route_data = {
                'company_id': row['company_id'],
                'Route_name': row['Route_name'],
                'taglist': row['taglist'],
                'location': row['location'], 
                'three_reasons': row['three_reasons'],
                'description': row['description']
            }
            Routes_data[row['Route_id']] = Route_data
        return Routes_data

    def cv_dataframe_to_dict(self, cv_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        cv_data = {}
        for i, row in cv_df.iterrows():
            cv_data[i] = {
                'expertise': row['Category'],
                'Flight_details': row['Flight_details']
            }
        return cv_data

    def create_network_from_data(self) -> nx.MultiDiGraph:
        G = nx.MultiDiGraph(name='Routes graph', num_airliness=0, num_Routes=0, num_Flights=0,
                            Flight_to_Route=0, Flight_to_Flight=0, Route_to_Route=0,
                            airlines_to_airlines=0, expertise_match=0, num_apply=0, num_favorite=0)

        for airlines_id, airlines_data in self.airliness_data.items():
            G.add_node(airlines_id, node_type='airlines', **airlines_data)
            G.graph['num_airliness'] += 1

        for Route_id, Route_data in self.Routes_data.items():
            G.add_node(Route_id, node_type='Route', **Route_data)
            G.graph['num_Routes'] += 1
            G.add_edge(Route_id, Route_data['company_id'], weight=constants.POSTED_WEIGHT, edge_type='posted')
            G.add_edge(Route_data['company_id'], Route_id, weight=constants.POSTED_WEIGHT, edge_type='posted')

        for _, Flight_data in self.cv_data.items():
            Flight_id = 'Flight-%d' % G.graph['num_Flights']
            G.add_node(Flight_id, node_type='Flight', **Flight_data)
            G.graph['num_Flights'] += 1
        return G

    def get_all_document_from_graph(self) -> List[str]:
        all_documents = []
        for _, node_data in self.G.nodes.items():
            if not node_data:
                print(_)
                break
            if node_data['node_type'] == 'airlines':
                all_documents.append(' '.join([str(node_data['overview']), str(node_data['benefit'])]))
            elif node_data['node_type'] == 'Route':
                all_documents.append(' '.join([str(node_data['three_reasons']), str(node_data['description'])]))
            elif node_data['node_type'] == 'Flight':
                all_documents.append(node_data['Flight_details'])
            else:
                continue
        return all_documents

    def get_lsa(self) -> latent_semantic_analysis.LSA:
        if os.path.isfile(constants.LSA_COMPARER_PATH):
            logger.info(f'Loading LSA comparer from {constants.LSA_COMPARER_PATH}')
            with open(constants.LSA_COMPARER_PATH, 'rb') as f:
                self.lsa = pickle.load(f)
        else:
            all_documents = self.get_all_document_from_graph()
            all_texts = ' '.join(all_documents)
            vocab = latent_semantic_analysis.make_vocab(all_texts, min_word_count=10)
            self.lsa = latent_semantic_analysis.LSA(vocab, all_documents, constants.NUM_REDUCED_FEATURES)
            self.lsa.do_work()
            logger.info(f'Saving LSA comparer to {constants.LSA_COMPARER_PATH}')
            with open(constants.LSA_COMPARER_PATH, 'wb') as f:
                pickle.dump(self.lsa, f, pickle.HIGHEST_PROTOCOL)

    def vectorize_nodes(self) -> None:
        for node_name in self.G:
            node = self.G.nodes[node_name]
            type = node['node_type']
            document = None
            if type == 'airlines':
                document = [str(node['overview']), str(node['expertise']), str(node['benefit'])]
            elif type == 'Route':
                document = [str(node['three_reasons']), str(node['description'])]
            elif type == 'Flight':
                document = [str(node['expertise']), str(node['Flight_details'])]
            if document is None:
                logger.info(f'Node {node} has no information to vectorize')
                self.G.nodes[node_name]['reduced_tfidf'] = np.array([])
                continue
            document = ' '.join(document)
            vector = self.lsa.vectorize(document)
            self.G.nodes[node_name]['reduced_tfidf'] = vector

    def create_keywords_for_nodes(self) -> None:
        processor = lambda x: x.lower().translate(str.maketrans('', '', string.punctuation)).split()
        for node_name in self.G:
            node = self.G.nodes[node_name]
            type = node['node_type']
            document = None
            if type == 'airlines':
                document = [str(node['overview']), str(node['expertise']), str(node['benefit']), str(node['company_name'])]
            elif type == 'Route':
                document = [str(node['three_reasons']), str(node['description']), str(node['Route_name'])]
            elif type == 'Flight':
                document = [str(node['expertise']), str(node['Flight_details'])]
            document = ' '.join(document)
            keywords = processor(document)
            keywords = ' '.join(keywords).split()
            keywords = set(keywords)
            self.G.nodes[node_name]['keywords'] = keywords

    def get_k_neighbors(self, data: np.ndarray, label: np.ndarray, k: int) -> Tuple[neighbors.KNeighborsClassifier, List[List[int]]]:
        knn = neighbors.KNeighborsClassifier(10, metric='euclidean')
        knn.fit(data, label)
        all_neighbors = []
        for point in data:
            nbs = knn.kneighbors(point.reshape(1, -1), k, return_distance=False)
            all_neighbors.append(nbs)
        return knn, all_neighbors

    def add_relations_edges(self, method='cosine') -> None:
        if method not in ['knn', 'cosine']:
            raise ValueError('Method must be either `knn` or `cosine`')
        airlines_node_names = [key for key, item in self.G.nodes.items() if item['node_type'] == 'airlines']
        Route_node_names = [key for key, item in self.G.nodes.items() if item['node_type'] == 'Route']
        Flight_node_names = [key for key, item in self.G.nodes.items() if item['node_type'] == 'Flight']
        airlines_vectors = [self.G.nodes[airlines]['reduced_tfidf'] for airlines in airlines_node_names]
        airlines_vectors = np.array(airlines_vectors).reshape(len(airlines_node_names), -1)
        Route_vectors = [self.G.nodes[Route]['reduced_tfidf'] for Route in Route_node_names]
        Route_vectors = np.array(Route_vectors).reshape(len(Route_node_names), -1)
        Flight_vectors = [self.G.nodes[Flight]['reduced_tfidf'] for Flight in Flight_node_names]
        Flight_vectors = np.array(Flight_vectors).reshape(len(Flight_node_names), -1)
        if method == 'knn':
            num_airlines_neighbors = int(constants.NEIGHBOR_RATIO * len(airlines_node_names))
            self.airlines_knn, airlines_neighbors = self.get_k_neighbors(airlines_vectors, np.arange(len(airlines_node_names)), num_airlines_neighbors)
            num_Route_neighbors = int(constants.NEIGHBOR_RATIO * len(Route_node_names))
            self.Route_knn, Route_neighbors = self.get_k_neighbors(Route_vectors, np.arange(len(Route_node_names)), num_Route_neighbors)
            num_Flight_neighbors = int(constants.NEIGHBOR_RATIO * len(Flight_node_names))
            self.Flight_knn, Flight_neighbors = self.get_k_neighbors(Flight_vectors, np.arange(len(Flight_node_names)), num_Flight_neighbors)
            for i, nbs in enumerate(airlines_neighbors):
                this_airlines = airlines_node_names[i]
                for nb_index in nbs[0]:
                    nb_name = airlines_node_names[nb_index]
                    if not self.G.has_edge(this_airlines, nb_name):
                        self.G.add_edge(this_airlines, nb_name, edge_type='airlines_to_airlines', weight=constants.SIMILAR_WEIGHT)
                        self.G.graph['airlines_to_airlines'] += 1
            for i, nbs in enumerate(Route_neighbors):
                this_Route = Route_node_names[i]
                for nb_index in nbs[0]:
                    nb_name = Route_node_names[nb_index]
                    if not self.G.has_edge(this_Route, nb_name):
                        self.G.add_edge(this_Route, nb_name, edge_type='Route_to_Route', weight=constants.SIMILAR_WEIGHT)
                        self.G.graph['Route_to_Route'] += 1
            for i, nbs in enumerate(Flight_neighbors):
                this_Flight = Flight_node_names[i]
                for nb_index in nbs[0]:
                    nb_name = Flight_node_names[nb_index]
                    if not self.G.has_edge(this_Flight, nb_name):
                        self.G.add_edge(this_Flight, nb_name, edge_type='Flight_to_Flight', weight=constants.SIMILAR_WEIGHT)
                        self.G.graph['Flight_to_Flight'] += 1
            pm_num_neigbors = int(constants.PROFILE_MATCHED_NEIHBOR_RATIO * len(Flight_node_names))
            for i, vector in enumerate(Flight_vectors):
                this_Flight = Flight_node_names[i]
                nbs = self.Route_knn.kneighbors(vector.reshape(1, -1), pm_num_neigbors, return_distance=False)
                for nb_index in nbs[0]:
                    nb_name = Route_node_names[nb_index]
                    if not self.G.has_edge(this_Flight, nb_name):
                        self.G.add_edge(this_Flight, nb_name, edge_type='Flight_to_Route', weight=constants.PROFILE_MATCH_WEIGHT)
                        self.G.graph['Flight_to_Route'] += 1
        if method == 'cosine':
            for i, id1 in enumerate(airlines_node_names):
                id1_vector = self.G.nodes[id1]['reduced_tfidf']
                for id2 in airlines_node_names[i+1:]:
                    id2_vector = self.G.nodes[id2]['reduced_tfidf']
                    sim = 1 - distance.cosine(id1_vector, id2_vector)
                    if sim >= constants.COSINE_SIMILARITY_THRESHOLD:
                        self.G.add_edge(id1, id2, edge_type='airlines_to_airlines', weight=constants.airlines_TO_airlines_WEIGHT, cosine_similarity=sim)
                        self.G.add_edge(id2, id1, edge_type='airlines_to_airlines', weight=constants.airlines_TO_airlines_WEIGHT, cosine_similarity=sim)
                        self.G.graph['airlines_to_airlines'] += 1
            for i, id1 in enumerate(Route_node_names):
                id1_vector = self.G.nodes[id1]['reduced_tfidf']
                for id2 in Route_node_names[i+1:]:
                    id2_vector = self.G.nodes[id2]['reduced_tfidf']
                    sim = 1 - distance.cosine(id1_vector, id2_vector)
                    if sim >= constants.COSINE_SIMILARITY_THRESHOLD:
                        self.G.add_edge(id1, id2, edge_type='Route_to_Route', weight=constants.Route_TO_Route_WEIGHT, cosine_similarity=sim)
                        self.G.add_edge(id2, id1, edge_type='Route_to_Route', weight=constants.Route_TO_Route_WEIGHT, cosine_similarity=sim)
                        self.G.graph['Route_to_Route'] += 1
            for i, id1 in enumerate(Flight_node_names):
                id1_vector = self.G.nodes[id1]['reduced_tfidf']
                for id2 in Flight_node_names[i+1:]:
                    id2_vector = self.G.nodes[id2]['reduced_tfidf']
                    sim = 1 - distance.cosine(id1_vector, id2_vector)
                    if sim >= constants.COSINE_SIMILARITY_THRESHOLD:
                        self.G.add_edge(id1, id2, edge_type='Flight_to_Flight', weight=constants.Flight_TO_Flight_WEIGHT, cosine_similarity=sim)
                        self.G.add_edge(id2, id1, edge_type='Flight_to_Flight', weight=constants.Flight_TO_Flight_WEIGHT, cosine_similarity=sim)
                        self.G.graph['Flight_to_Flight'] += 1
            for i, id1 in enumerate(Flight_node_names):
                id1_expertise = self.G.nodes[id1]['expertise'] 
                for id2 in Flight_node_names[i+1:]:
                    id2_expertise = self.G.nodes[id2]['expertise']
                    if id1_expertise == id2_expertise:
                        self.G.add_edge(id1, id2, edge_type='expertise_match', weight=constants.EXPERTISE_MATCH_WEIGHT)
                        self.G.add_edge(id2, id1, edge_type='expertise_match', weight=constants.EXPERTISE_MATCH_WEIGHT)
                        self.G.graph['expertise_match'] += 1
                       
    def build(self) -> None:
        logger.info('Start building the master Graph...')
        self.G = self.create_network_from_data()
        logger.info('Master Graph is built.')
        logger.info('Creating LSA comparer')
        self.get_lsa() 
        logger.info('Compute tf-idf vector for every node')
        self.vectorize_nodes()
        logger.info('Creating keywords for nodes...')
        self.create_keywords_for_nodes()
        logger.info('Adding relations edges...')
        self.add_relations_edges(method=constants.SIMILARITY_METHOD)
        logger.info('Network is built.')


if __name__ == '__main__':

    if os.path.isfile(constants.NETWORK_BUILDER_SAVE_PATH):
        logger.info(f'Loading network from {constants.NETWORK_BUILDER_SAVE_PATH}')
        with open(constants.NETWORK_BUILDER_SAVE_PATH, 'rb') as f:
            network = pickle.load(f)

    else:
        network = NetworkBuilder(constants.airlinesS_DATA_PATH,
                            constants.RouteS_DATA_PATH,
                            constants.CV_DATAPATH)

        network.build()

        logger.info(f'saving network builder object to {constants.NETWORK_BUILDER_SAVE_PATH}')

        with open(constants.NETWORK_BUILDER_SAVE_PATH, 'wb') as f:
            pickle.dump(network, f, pickle.HIGHEST_PROTOCOL)
