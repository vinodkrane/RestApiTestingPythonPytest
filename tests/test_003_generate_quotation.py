"""Create quotes tests."""
import logging
import pytest
from session.httpsession import HttpRequestExecutor
from tests.test_001_create_member import TestCreateMember

LOG = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def get_request_instance(request):
    """Pytest fixture to get request object."""
    request.cls.request = HttpRequestExecutor()
    return request


@pytest.mark.usefixtures("get_request_instance")
class TestCreateQuotation:
    """Tests to validate create quotation feature."""

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_080_create_a_quote_with_loan_amount_1000(self):
        """Return true if quote is created for loan amount 1000."""
        payload = {
          "currentSalary": 30000,
          "amountToBorrow": 1000,
          "termLength": 24
        }

        LOG.debug('memberId=%r', TestCreateMember.get_member_id())
        query_params = {'memberId': TestCreateMember.get_member_id()}
        response = self.request.post_api('/api/quote', payload, query_params)

        # Validate status code and response headers
        assert response.status_code == 200, "Create quote is failed!"
        resp_body = response.json()

        # Validate Json response
        assert resp_body['quoteId'] is not None
        assert resp_body['quoteOffered'] == True
        assert resp_body['amountToBorrow'] == 1000

    @pytest.mark.regression
    def test_090_create_a_quote_with_loan_amount_25000(self):
        """Return true if quote is created."""
        payload = {
          "currentSalary": 30000,
          "amountToBorrow": 25000,
          "termLength": 24
        }

        LOG.debug('memberId=%r', TestCreateMember.get_member_id())
        query_params = {'memberId': TestCreateMember.get_member_id()}
        response = self.request.post_api('/api/quote', payload, query_params)

        # Validate status code and response headers
        assert response.status_code == 200, "Create quote is failed!"
        resp_body = response.json()

        # Validate Json response
        assert resp_body['quoteId'] is not None
        assert resp_body['quoteOffered'] == True
        assert resp_body['amountToBorrow'] == 25000

    @pytest.mark.regression
    def test_100_create_a_quote_with_loan_amount_12000(self):
        """Verify that the micro-service can create a quote."""
        payload = {
          "currentSalary": 30000,
          "amountToBorrow": 12000,
          "termLength": 24
        }

        LOG.debug('memberId=%r', TestCreateMember.get_member_id())
        query_params = {'memberId': TestCreateMember.get_member_id()}
        response = self.request.post_api('/api/quote', payload, query_params)

        # Validate status code and response headers
        assert response.status_code == 200, "Create quote is failed."
        resp_body = response.json()

        # Validate Json response
        assert resp_body['quoteId'] is not None
        assert resp_body['quoteOffered'] == True
        assert resp_body['amountToBorrow'] == 12000

    @pytest.mark.regression
    def test_110_create_a_quote_with_loan_amount_999(self):
        """Verify that the micro-service cannot create a quote for invalid value."""
        payload = {
          "currentSalary": 30000,
          "amountToBorrow": 999,
          "termLength": 24
        }

        LOG.debug('memberId=%r', TestCreateMember.get_member_id())
        query_params = {'memberId': TestCreateMember.get_member_id()}
        response = self.request.post_api('/api/quote', payload, query_params)

        # Validate status code and response headers
        assert response.status_code == 400, "Create quote is successful!"

    @pytest.mark.regression
    def test_120_create_a_quote_with_loan_amount_25001(self):
        """Verify that the micro-service cannot create a quote for invalid value."""
        payload = {
          "currentSalary": 30000,
          "amountToBorrow": 25001,
          "termLength": 24
        }

        LOG.debug('memberId=%r', TestCreateMember.get_member_id())
        query_params = {'memberId': TestCreateMember.get_member_id()}
        response = self.request.post_api('/api/quote', payload, query_params)

        # Validate status code and response headers
        assert response.status_code == 400, "Create quote is successful!"

    @pytest.mark.regression
    def test_130_create_a_quote_with_loan_amount_negative(self):
        """Verify that the micro-service can create a quote."""
        payload = {
          "currentSalary": 30000,
          "amountToBorrow": -5000,
          "termLength": 24
        }

        LOG.debug('memberId=%r', TestCreateMember.get_member_id())
        query_params = {'memberId': TestCreateMember.get_member_id()}
        response = self.request.post_api('/api/quote', payload, query_params)

        # Validate status code and response headers
        assert response.status_code == 400, "Create quote is successful!"

    @pytest.mark.regression
    def test_140_create_a_quote_with_loan_with_non_existing_member(self):
        """Verify that the micro-service cannot create a quote for non-existent member."""
        payload = {
          "currentSalary": 30000,
          "amountToBorrow": 5000,
          "termLength": 24
        }
        member_id = 'a4eb85f3-38c5-4af1-98ed-46424d45pwe1'
        query_params = {'memberId': member_id}
        response = self.request.post_api('/api/quote', payload, query_params)

        # Validate status code and response headers
        assert response.status_code == 404, "Create quote is successful!"
