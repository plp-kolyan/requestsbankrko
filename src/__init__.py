import os
from dotenv import load_dotenv


load_dotenv()
path_to_env = os.environ.get('path_to_env')
if path_to_env:
    load_dotenv(dotenv_path=path_to_env)
