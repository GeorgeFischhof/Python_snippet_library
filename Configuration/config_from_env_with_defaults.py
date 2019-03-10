
"""

Returns a config value

Config value can came from environment, or from default config

Cases:

    - environment variable: no,  default value: yes  --  default value is returned

    - environment variable: yes, default value: yes  --  environment variable is returned with type of default value

    - environment variable: yes, default value: no   --  environment variable is returned as a string without casting

    - environment variable: no,  default value: no   --  returns None

"""

 

import os

 

 

class Defaults():

    VARIABLE_WITH_CAPITAL_LETTERS_TO_BE_SIMILAR_TO_ENVIRONMENT_VARIABLES = list()

 

 

def _get_casted_environment_value(key, value):

    if hasattr(Defaults, key) and not isinstance(getattr(Defaults,key), str):

        return eval(value)

    else:

        return value

 

 

def get_config(key: str):

    key = key.upper()

    environment_value = os.getenv(key)

    if environment_value is not None:

        return _get_casted_environment_value(key, environment_value)

    else:

        return getattr(Defaults, key, None)

 

#           #

# SELFTESTS #

#           #

 

 

def test_env_no_default_yes():

    Defaults.QWERTYUIOP_DICT = {'QWERTYUIOP': 'qwertyuiop'}

    config = get_config('QWERTYUIOP_DICT')

    assert isinstance(config, dict)

    assert config['QWERTYUIOP'] == 'qwertyuiop'

    del Defaults.QWERTYUIOP_DICT

 

 

def test_env_yes_default_yes():

    Defaults.QWERTYUIOP_LIST = ['one', 'two', 'three']

    env = os.environ

    env['QWERTYUIOP_LIST'] = "['four', 'five', 'six']"

    config = get_config('QWERTYUIOP_LIST')

    assert isinstance(config, list)

    assert config == ['four', 'five', 'six']

    del Defaults.QWERTYUIOP_LIST

    del env['QWERTYUIOP_LIST']

 

 

def test_env_yes_default_no():

    env = os.environ

    env['QWERTYUIOP_LIST'] = "['four', 'five', 'six']"

    config = get_config('QWERTYUIOP_LIST')

    assert isinstance(config, str)

    assert config == "['four', 'five', 'six']"

    del env['QWERTYUIOP_LIST']

 

 

def test_env_no_default_no():

    config = get_config('NON_EXISTENT_ENVIRONMENT_VARIABLE')

    assert config is None

 

 

"""

# to test the function, you can execute above tests in a test framework or

# you can remove the triple quotes from around these lines

 

test_env_no_default_yes()

test_env_yes_default_yes()

test_env_yes_default_no()

test_env_no_default_no()

 

"""
