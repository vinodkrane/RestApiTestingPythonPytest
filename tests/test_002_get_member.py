"""Get member tests."""
import logging
import pytest
from config.schema import *
from jsonschema import validate
from session.httpsession import HttpRequestExecutor
from tests.test_001_create_member import TestCreateMember

LOG = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def get_request_instance(request):
    """Pytest fixture to get request object."""
    request.cls.request = HttpRequestExecutor()
    return request


@pytest.mark.usefixtures("get_request_instance")
class TestGetMember:
    """Tests to validate get member feature."""

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_060_get_member(self):
        """Return a member by member_id."""
        query_params = {'memberId': TestCreateMember.get_member_id()}
        res = self.request.get_api('/api/member', query_params)
        res_body = res.json()

        # Validate status code. memberid, response headers
        assert res.status_code == 200, "Result not found!"
        assert res_body['memberId'] == TestCreateMember.get_member_id(), "MemberId is not matched!"
        assert res_body['firstName'] == 'Tony', "No data exists for first name."
        assert res_body['lastName'] == 'Tester', "No data exists for last name."
        assert res_body['emailAddress'] == 'tony.tester@zopa.com', "No data exists for email."
        validate(instance=res_body, schema=GetMemberSchema)

    @pytest.mark.regression
    def test_070_get_non_existing_member(self):
        """Return non existing member by mmember_id."""
        # Send get member request
        member_id = 'a4eb85f3-38c5-4af1-98ed-46424d45cf21'
        params = {'memberId': member_id}
        resp = self.request.get_api('/api/member', params)
        res_body = resp.json()

        # Validate status code. member_id, response headers
        assert resp.status_code == 404, "Result not found!"
