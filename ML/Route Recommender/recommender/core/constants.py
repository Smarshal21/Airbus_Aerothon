
LOG_FILE_PATH = '/home/samanwith/Desktop/Route_recommender/recommender/core/log.txt'
airlinesS_DATA_PATH = '/home/samanwith/Desktop/Route_recommender/data/companies.csv'
RouteS_DATA_PATH = '/home/samanwith/Desktop/Route_recommender/data/Routes.csv'
CV_DATAPATH = '/home/samanwith/Desktop/Route_recommender/data/cvdata/Flight_detailsDataSet.csv'
NETWORK_DATA_PATH = '/home/samanwith/Desktop/Route_recommender/data/network_data'
NETWORK_BUILDER_SAVE_PATH = '/home/samanwith/Desktop/Route_recommender/data/network_data/network_builder.pkl'

VOCAB_PATH = '/home/samanwith/Desktop/Route_recommender/data/network_data/vocab.json'
LSA_COMPARER_PATH = '/home/samanwith/Desktop/Route_recommender/data/network_data/lsa.pkl'


# Edge weights
#  
POSTED_WEIGHT = 1
APPLIED_WEIGHT = 2

airlines_TO_airlines_WEIGHT = 1
Route_TO_Route_WEIGHT = 1
Flight_TO_Flight_WEIGHT = 1
Flight_TO_Route_WEIGHT = 1

PROFILE_MATCH_WEIGHT = 1
EXPERTISE_MATCH_WEIGHT = 1

FAVORITE_WEIGHT = 1
LIKE_WEIGHT  = 0.5
VISIT_WEIGHT = 0.2


NUM_REDUCED_FEATURES = 0.3
# How many neighbors should one node connect to, if it's float, it's the ratio
# of all node considered. 
NEIGHBOR_RATIO = 0.01
PROFILE_MATCHED_NEIHBOR_RATIO = 0.01
SIMILARITY_METHOD = 'cosine'

# Two nodes are considered similar if they have the cosine similarity > this threshold
COSINE_SIMILARITY_THRESHOLD = 0.4
PROFILE_MATCHED_SIMILARITY_THRESDHOLD = 0.4

# damping probability for PageRank
alpha = 0.5