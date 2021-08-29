"""Schema definition file."""

CreateMemberSchema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "memberId": {
      "type": "string"
    },
    "firstName": {
      "type": "string"
    },
    "lastName": {
      "type": "string"
    },
    "address": {
      "type": "object",
      "properties": {
        "firstLine": {
          "type": "string"
        },
        "town": {
          "type": "string"
        },
        "postCode": {
          "type": "string"
        }
      },
      "required": [
        "firstLine",
        "town",
        "postCode"
      ]
    },
    "emailAddress": {
      "type": "string"
    },
    "jobTitle": {
      "type": "string"
    },
    "memberFullName": {
      "type": "string"
    }
  },
  "required": [
    "memberId",
    "firstName",
    "lastName",
    "address",
    "emailAddress",
    "jobTitle",
    "memberFullName"
  ]
}

GetMemberSchema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "memberId": {
      "type": "null"
    },
    "firstName": {
      "type": "null"
    },
    "lastName": {
      "type": "null"
    },
    "address": {
      "type": "object",
      "properties": {
        "firstLine": {
          "type": "null"
        },
        "town": {
          "type": "string"
        },
        "postCode": {
          "type": "null"
        }
      },
      "required": [
        "firstLine",
        "town",
        "postCode"
      ]
    },
    "emailAddress": {
      "type": "null"
    },
    "jobTitle": {
      "type": "null"
    },
    "memberFullName": {
      "type": "null"
    }
  },
  "required": [
    "memberId",
    "firstName",
    "lastName",
    "address",
    "emailAddress",
    "jobTitle",
    "memberFullName"
  ]
}
