import json
import os
import json
from pathlib import Path

from . import config

class CacheHandler:
    """ Simple cache handler. Allows (temporary) information to be written to a file in the cache-directory. """
    
    def __init__(self, fail_silently: bool = False) -> None:
        root_dir = Path(__file__).parent.absolute()
        self.cache_dir = f'{root_dir}/cache'
        
        self.fail_silently = fail_silently
    
    def write(self, key: str, value: str, overwrite: bool = True) -> bool:
        """ Write to a file in the cache-directory.
        Key: unique key where the value will be stored under.
        Value: the value associated with the key.
        Overwrite: allow to overwrite the value if the key is already present. Default true.
        """
        
        if type(value) != dict: raise ValueError('Value must be of type "dict"')
        
        full_path = f'{self.cache_dir}/{key}.txt'
        
        if os.path.exists(full_path) and not overwrite:
            if self.fail_silently: return False
            raise ValueError(f'"{key}" already exists in this cache, overwrite is set to false.')
        
        with open(full_path, 'w') as cache_file:
            cache_file.write(json.dumps(value))
            config.CACHE[key] = value
        
        return True
        
    def get(self, key: str, default: bool = None) -> dict:
        """ Get a value from the corresponding key.
        Key: unique key that holds the returning value.
        Returns the value or default if value can't be found. Default value is None.
        """
        
        if key in config.CACHE: return config.CACHE[key]
        
        full_path = f'{self.cache_dir}/{key}.txt'
        
        if not os.path.exists(full_path):
            if self.fail_silently: return default
            raise ValueError(f'"{key}" does not exist inside cache.')
        
        with open(full_path, 'r') as cache_file:
            str_value = cache_file.read()
        
        value = json.loads(str_value)
        return value