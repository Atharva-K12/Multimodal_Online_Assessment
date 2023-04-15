SECRET_KEY = 'xyz'
MONGO_URI = 'mongodb://Sahil_Purohit:#Pass4mongodb@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority'
CLUSTER_THRESHOLD = 0.7
VIDEO_FOLDER = 'D:\\Multimodal_Online_Assessment\\backend\\videoFiles'

# # from dotenv import load_dotenv
# import os

# # load_dotenv()

# # MONGO_URI = 'mongodb://'+os.getenv('MONGO_USERNAME')+':'+os.getenv('MONGO_PASSWORD')+'@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority'


# # print(MONGO_URI)


# from dotenv import load_dotenv, main

# try:
#     load_dotenv()
# except main.DotEnvError as e:
#     print(f"Error loading .env file: {e}")

# MONGO_URI = f"mongodb://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@ac-hifbqdl-shard-00-00.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-01.11jbtg4.mongodb.net:27017,ac-hifbqdl-shard-00-02.11jbtg4.mongodb.net:27017/?ssl=true&replicaSet=atlas-bzogsd-shard-0&authSource=admin&retryWrites=true&w=majority"



# import yaml

# with open('config.yaml', 'r') as f:
#     config = yaml.safe_load(f)

# MONGO_URI = f"mongodb://{config['mongo_username']}:{config['mongo_password']}@{config['mongo_host']}/?{config['mongo_options']}"
