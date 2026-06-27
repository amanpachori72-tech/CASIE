# Sample code for CASIE to analyze
def database_connector():
    print("Connecting to core database...")
    return "DB_CONN_ACTIVE"

def user_authentication(user_id, token):
    # This function is heavily coupled (calls multiple things)
    db = database_connector()
    status = verify_token_signature(token)
    log_security_event(user_id, "LOGIN_ATTEMPT")
    return {"user": user_id, "authenticated": status}

def verify_token_signature(token):
    return True

def log_security_event(user_id, event_type):
    print(f"Log: User {user_id} triggered {event_type}")