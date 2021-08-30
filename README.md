# Python based RestApi Testing Framework - Pytest
## _Vinod Rane_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This is a sample Rest API test solution for Zopa Testing challenge. Tests are written using a combination of Pytest, Python.

## Framework Specifications
1. The test design is based on the concept of AAA design pattern (Arrange Act Assert).
2. Simple templating of HTTP request bodies, URLs, and validators, with user variables
2. The pytest framework makes it easy to write tests, and scales to support complex functional testing.
3. API calls & validations are made using Python requests library.
4. Framework uses jsonschema to validate the received JSON.
5. You can mark test functions that you expect to fail so framework can deal with them accordingly.
6. You can run certain set of tests by marking the tests e.g. smoke, regression
7. Framework generates comprehensive logging and html, junit xml reports.  
8. Pytest generated Junit XML result files can be processed by Jenkins with the JUnit plugin to display results of the tests.

## Project structure

```sh
├───config
│   ├───config_loader.py
│   ├───schema.py 
│   └───setting.json
│
├───log
│    └───2021-08-29.19-49-23
│		├─────────test_001_create_member
│		│		├───TestCreateMember
│   		│		└───TestCreateMemberForNegativeTests				
│		├─────────test_002_get_member
│		│		└───TestGetMember
│		├─────────test_003_generate_quotation
│		│		└───TestCreateQuotation
│		└─────────main.log
├───results
│     └───html 
│	   └───index.html
│     └───junitxml
│	   └───junit.xml
├───session
│      └───httpsession.py
├───tests
│   ├───conftest.py
│   ├───test_001_create_member.py  
│   ├───test_002_get_member.py       
│   └───test_003_generate_quotation.py
└───requirement.txt			  
```

1. config - Read Configurations from JSON files
2. log - Test execution logs.
3. results - Test execution results. (HTML, junitxml)
4. session - The client to send HTTP requests.
5. tests - Unit tests set.

## Requirements
Python 3.8 and the following packages (all available via pip):
1. pytest
2. pytest-cov
3. jsonpath_rw
4. pylint
5. requests
6. jsonschema
7. pytest-html

Or install via requirements.txt file after cloning the project:
```sh
pip install -r requirements.txt
```

## Getting Started
1. git clone https://github.com/vinodkrane/RestApiTestingPythonPytest.git
2. cd RestApiTestingPythonPytest
3. pip install -r requirements.txt

## Running test
1. cd $project_directory
2. Open command prompt or terminal.
3. Run tests using following command.
    ```sh
	Run all Tests
        pytest -v --junitxml=results\junitxml\junit.xml --html=results\html\report.html
	
	Run tests in specific module
	pytest -v --junitxml=results\junitxml\junit.xml --html=results\html\report.html tests/test_001_create_member.py
	
	Run smoke tests
	pytest -v --junitxml=results\junitxml\junit.xml --html=results\html\report.html -m smoke
	
	Run regression tests
	pytest -v --junitxml=results\junitxml\junit.xml --html=results\html\report.html -m regression
	
	To run the code coverage report
	pytest --cov=src tests
    ```

## Results
1. Results can be viewed on console.
2. HTML reports are recorded at RestApiTestingPythonPytest/results/html/
3. junitxml reports are recorded at RestApiTestingPythonPytest/results/junitxml/

## Troubleshooting failures
1. Check the failures/warnings on console.
2. Check the logs generated at $project_home/log directory.
3. Debug the code.

## Tests automated
Create Member
1. Create create a member.
2. Return error if mandatory parameter firstname is missing.
3. Return error if mandatory parameter address is missing
4. Return error if mandatory parameter emailAddress is missing.
5. Return error if bad job title is provided.

Get Member
1. Return a member by member id.
2. Return non existing member by member id.

Create Quotation
1. Return true if quote is created for loan amount 1000.
2. Return true if quote is created for loan amount 25000.
3. Return true if quote is created for loan amount 12000.
4. Return false if quote is created for loan amount 999.
5. Return false if quote is created for loan amount 25001.
6. Return false if quote is created for loan amount -5000.
7. Return false if quote is created for non existing member.

## Application under test
A site for tracking the location of and getting fly-over notifications for the International Space Station.
https://qanat-quotes-public.staging.zopa.com/api/docs

## Contribution
1. Fork it!
2. Create your feature branch: git checkout -b my-new-feature
3. Commit your changes: git commit -am 'feature details'
4. Push to the branch: git push origin my-new-feature
5. Submit a pull request :D

## References
1. Python - for writing python code https://docs.python.org/3.8/
2. Python Requests Module - for write RESTful APIs tests( https://docs.python-requests.org/en/master/)
3. Coverage - for code coverage https://pypi.org/project/coverage/
