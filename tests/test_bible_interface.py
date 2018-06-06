from app.bible_interface import query_bible_api


def test_query_bible_api():

    passage_result = query_bible_api("John", 3, 16)
    assert type(passage_result) == str
    assert "For God so loved" in passage_result

