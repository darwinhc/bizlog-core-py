import pytest
from bisslog.exceptions.domain_exception import DomainException, NotFound, NotAllowed

def test_exception_hierarchy():
    """Verify that exceptions inherit correctly"""
    assert issubclass(NotFound, DomainException)
    assert issubclass(NotAllowed, DomainException)
    assert issubclass(DomainException, Exception)

def test_exception_instantiation():
    """Verifies that exceptions can be instantiated with the correct attributes"""
    exc = DomainException("general-error", "A general error occurred")
    assert exc.keyname == "general-error"
    assert exc.message == "A general error occurred"

    not_found_exc = NotFound("user-not-found", "User not found")
    assert isinstance(not_found_exc, DomainException)
    assert not_found_exc.keyname == "user-not-found"
    assert not_found_exc.message == "User not found"

    not_allowed_exc = NotAllowed("action-restricted", "You cannot perform this action")
    assert isinstance(not_allowed_exc, DomainException)
    assert not_allowed_exc.keyname == "action-restricted"
    assert not_allowed_exc.message == "You cannot perform this action"

def test_exception_catching():
    """Verify that exceptions can be captured correctly"""
    with pytest.raises(DomainException):
        raise NotFound("resource-missing", "Requested resource is missing")

    with pytest.raises(NotFound):
        raise NotFound("user-missing", "User does not exist")

    with pytest.raises(NotAllowed):
        raise NotAllowed("forbidden", "This action is not allowed")
