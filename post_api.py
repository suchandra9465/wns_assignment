import importlib.util
import requests

def import_function_from_git(url, function_name):

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch file content from Git repository")
    
    module_name = 'temp_module'
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)

    exec(response.text, module.__dict__)

    function = getattr(module, function_name)

    return function

git_raw_url = 'https://raw.githubusercontent.com/suchandra9465/wns/master/git_call_api.py'
function_name = 'fetch_data_from_mapping'

my_function = import_function_from_git(git_raw_url, function_name)

result = my_function("input.json", "wns_input_sheet - Sheet1.csv")
print(result)