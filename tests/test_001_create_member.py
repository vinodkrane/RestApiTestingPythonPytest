"""Create member tests."""
import logging
import pytest
from config.schema import *
from jsonschema import validate
from session.httpsession import HttpRequestExecutor

LOG = logging.getLogger(__name__)
MEMBER_ID = ""


@pytest.fixture(scope="class")
def get_request_instance(request):
    """Pytest fixture to get request object."""
    request.cls.request = HttpRequestExecutor()
    return request


@pytest.mark.usefixtures("get_request_instance")
class TestCreateMember:
    """Tests to validate create member feature."""

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_010_create_member(self):
        """Create create a member."""
        global MEMBER_ID
        payload = {
              "firstName": "Tony",
              "lastName": "Tester",
              "address": {
                "firstLine": "47-49 Cottons Centre",
                "town": "London",
                "postCode": "SE1 2QG"
              },
              "emailAddress": "tony.tester@zopa.com",
              "jobTitle": "Tester/Breaker"
            }
        response = self.request.post_api('/api/member', payload)

        # Validate status code and response headers
        assert response.status_code == 201, "Member creation is failed."
        assert response.headers['Content-Type'] == "application/json"

        # Got a JSON response.
        assert response.json()

        # Validate Json response
        LOG.debug('resp.json=%r', response.json())
        resp_body = response.json()
        assert resp_body['memberId'] is not None, "Member id is none."

        MEMBER_ID = resp_body['memberId']
        LOG.debug('Member_id=%r', MEMBER_ID)
        assert resp_body['firstName'] == 'Tony', '\
                              No data exists for first name.'
        assert resp_body['lastName'] == 'Tester', "No data exists for name."
        assert resp_body['emailAddress'] == 'tony.tester@zopa.com', "\
                              No data exists for email."
        validate(instance=resp_body, schema=CreateMemberSchema)

    @staticmethod
    def get_member_id():
        """
        Getter method to return a member_id.

        No need to create member every time. Existing
        member_id can be reused in rest of the tests.
        """
        return MEMBER_ID


@pytest.mark.usefixtures("get_request_instance")
class TestCreateMemberForNegativeTests:
    """Tests to validate negative scenarios of create member feature."""

    @pytest.mark.regression
    def test_020_create_member_with_missing_name(self):
        """Return error if mandatory parameter firstname is missing."""
        payload = {
              "lastName": "Tester",
              "address": {
                "firstLine": "47-49 Cottons Centre",
                "town": "London",
                "postCode": "SE1 2QG"
              },
              "emailAddress": "tony.tester@zopa.com",
              "jobTitle": "Tester/Breaker"
            }
        response = self.request.post_api('/api/member', payload)

        # Validate status code and response headers
        assert response.status_code == 400, "Member creation failed!"
        assert response.headers["Content-Type"] == "application/json"

        # Got a JSON response.
        assert response.json()

        # Validate Json response
        LOG.debug('resp.json=%r', response.json())
        resp_body = response.json()
        assert resp_body['errors']['firstName'] == \
               "\'firstName\' is a required property"

    @pytest.mark.regression
    def test_030_create_member_with_missing_address(self):
        """Return error if mandatory parameter address is missing."""
        payload = {
              "firstName": "Tom",
              "lastName": "Tester",
              "address": {
                "firstLine": "47-49 Cottons Centre",
                "postCode": "SE1 2QG"
              },
              "emailAddress": "tony.tester@zopa.com",
              "jobTitle": "Tester/Breaker"
            }
        response = self.request.post_api('/api/member', payload)

        # Validate status code and response headers
        assert response.status_code == 400, "Member creation failed!"
        assert response.headers["Content-Type"] == "application/json"

        # Got a JSON response.
        assert response.json()

        # Validate Json response
        LOG.debug('resp.json=%r', response.json())
        resp_body = response.json()
        assert resp_body['errors']['address.town'] == \
               "'town' is a required property"

    @pytest.mark.regression
    def test_040_create_member_with_missing_emailAddress(self):
        """Return error if mandatory parameter emailAddress is missing."""
        payload = {
              "firstName": "Tom",
              "lastName": "Tester",
              "address": {
                "firstLine": "47-49 Cottons Centre",
                "town": "London",
                "postCode": "SE1 2QG"
              },
              "jobTitle": "Tester/Breaker"
            }
        response = self.request.post_api('/api/member', payload)

        # Validate status code and response headers
        assert response.status_code == 400, "Member creation failed!"
        assert response.headers["Content-Type"] == "application/json"

        # Got a JSON response.
        assert response.json()

        # Validate Json response
        LOG.debug('resp.json=%r', response.json())
        resp_body = response.json()
        assert resp_body['errors']['emailAddress'] == \
               "\'emailAddress\' is a required property"

    @pytest.mark.regression
    def test_050_create_member_with_bad_job_title(self):
        """Return error if bad job title is provided."""
        payload = {
              "firstName": "Tom",
              "lastName": "Tester",
              "address": {
                "firstLine": "47-49 Cottons Centre",
                "town": "London",
                "postCode": "SE1 2QG"
              },
              "emailAddress": "tony.tester@zopa.com",
              "jobTitle": "Invalid job title. Invalid job title. Invalid job title. Invalid job title. Invalid job title. Invalid job title. "
            }
        response = self.request.post_api('/api/member', payload)

        # Validate status code and response headers
        assert response.status_code == 400, "Member creation failed!"
        assert response.headers["Content-Type"] == "application/json"

        # Got a JSON response.
        assert response.json()

        # Validate Json response
        LOG.debug('resp.json=%r', response.json())
        resp_body = response.json()
        assert resp_body['message'] == \
               "jobTitle must be <= 20 characters"
