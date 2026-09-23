import logging

logger          = logging.getLogger("rbac_audit")
handler         = logging.FileHandler("rbac_audit.log")
formatter       = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_role_assignment(user, role):
    logger.info(f"User {user.username} assigned to role {role.name}")
