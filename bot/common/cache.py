user_agent_dict = {}


def get_agent(user_id):
    return user_agent_dict.get(user_id, None)
