from datetime import datetime

def log_action(user, role, action, status):
    with open("audit.log", "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now()} | user={user} | role={role} | action={action} | status={status}\n"
        )

log_action("othmane", "reader", "get_item", "AUTHORIZED")
log_action("othmane", "reader", "delete_item", "DENIED")

print("Journal d'audit créé avec succès.")