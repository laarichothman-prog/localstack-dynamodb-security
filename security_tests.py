from access_control import ROLE_PERMISSIONS

def test_reader_permissions():
    assert "get_item" in ROLE_PERMISSIONS["reader"]
    assert "scan" in ROLE_PERMISSIONS["reader"]
    assert "delete_item" not in ROLE_PERMISSIONS["reader"]
    print("Test reader réussi.")

def test_writer_permissions():
    assert "put_item" in ROLE_PERMISSIONS["writer"]
    assert "get_item" in ROLE_PERMISSIONS["writer"]
    assert "delete_item" not in ROLE_PERMISSIONS["writer"]
    print("Test writer réussi.")

def test_admin_permissions():
    assert "put_item" in ROLE_PERMISSIONS["admin"]
    assert "get_item" in ROLE_PERMISSIONS["admin"]
    assert "delete_item" in ROLE_PERMISSIONS["admin"]
    print("Test admin réussi.")

test_reader_permissions()
test_writer_permissions()
test_admin_permissions()

print("Tous les tests de sécurité sont réussis.")