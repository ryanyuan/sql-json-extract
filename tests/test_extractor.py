import json
import unittest

import sqlparse
from sje import extractor

ONE_LEVEL_JSON = [
    {"name": "name", "type": "STRING"},
    {"name": "age", "type": "NUMERIC"},
]

NESTED_JSON = [
    {"name": "name", "type": "STRING"},
    {
        "name": "metadata",
        "type": "RECORD",
        "fields": [
            {
                "name": "skills",
                "type": "RECORD",
                "fields": [
                    {
                        "name": "java",
                        "type": "RECORD",
                        "fields": [{"name": "rating", "type": "NUMERIC"}],
                    }
                ],
            },
            {"name": "age", "type": "NUMERIC"},
        ],
    },
]

NESTED_JSON_FLATTEN = [
    {"name": "name", "type": "STRING"},
    {"name": "metadata_skills_java_rating", "type": "NUMERIC"},
    {"name": "metadata_age", "type": "NUMERIC"},
]

TRAILER_CLAUSE = "from `project:dataset.table limit 1000"

NESTED_JSON_SQL = "SELECT CAST(name AS STRING), \
       CAST(JSON_EXTRACT(metadata, '$.skills.java.rating') AS NUMERIC) AS metadata_skills_java_rating, \
       CAST(JSON_EXTRACT(metadata, '$.age') AS NUMERIC) AS metadata_age"


class TestExtractor(unittest.TestCase):
    def test_flatten_all_empty(self):
        result = extractor.flatten_all([])
        assert result == []

    def test_flatten_all_one_level(self):
        result = extractor.flatten_all(ONE_LEVEL_JSON)
        assert result == ONE_LEVEL_JSON

    def test_flatten_all_nested(self):
        result = extractor.flatten_all(NESTED_JSON)
        assert result == NESTED_JSON_FLATTEN

    def test_flatten_all_as_sql_nested(self):
        result = extractor.flatten_all_as_sql(NESTED_JSON)
        nested_json_sql_parsed = sqlparse.format(
            NESTED_JSON_SQL, reindent=True, keyword_case="upper"
        )
        assert result == nested_json_sql_parsed

    def test_flatten_all_as_sql_nested_with_trailer_clause(self):
        result = extractor.flatten_all_as_sql(
            NESTED_JSON, trailer_clause=TRAILER_CLAUSE
        )
        nested_json_sql_parsed = sqlparse.format(
            f"{NESTED_JSON_SQL} {TRAILER_CLAUSE}", reindent=True, keyword_case="upper"
        )
        assert result == nested_json_sql_parsed

if __name__ == '__main__':
    unittest.main()