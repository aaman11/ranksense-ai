PERSONAS = [
    {"id": "budget", "label": "Budget Shopper", "system": "You prefer cheap products"},
    {"id": "premium", "label": "Premium Buyer", "system": "You prefer premium products"},
    {"id": "expert", "label": "Expert", "system": "You prefer high-quality validated products"},
]

def build_prompt(persona, query):
    system = persona["system"]
    user = f'Query: "{query}". Give top 5 brands ranked.'
    return system, user
