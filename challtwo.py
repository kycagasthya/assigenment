# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.

def get_nested_value(data: dict, key: str) -> any:
    """
    Get the value of a key in a nested object (dictionary)
    """
    keys = key.split("/")
    result = data
    for k in keys:
        print (k)
        result = result.get(k)
        if result is None:
            return None
    return result

data = {"a": {"b": {"c": {"d":"yashwanth"}}}}
key = "a/b/c/d"
value = get_nested_value(data, key)
print(value) # "d"

