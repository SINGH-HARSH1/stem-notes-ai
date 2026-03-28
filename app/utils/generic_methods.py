import uuid



def generate_unique_id(input_prefix: str) -> str:
    unique_id = input_prefix + str(uuid.uuid4())
    return unique_id
