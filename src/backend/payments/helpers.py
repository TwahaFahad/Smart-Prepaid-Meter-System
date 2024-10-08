import uuid


def generate_reference():
    code = str(uuid.uuid4()).replace("-", "")[:30]
    return code
