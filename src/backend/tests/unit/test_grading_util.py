from app.utils import parse_result


def test_parse_result():
    """测试评分结果解析"""
    results = [
        "score: 100/100",
        "score: 0/100",
        "score: 60/100",
        "score: 99/100",
    ]
    expected = [100, 0, 60, 99]

    for result, expect in zip(results, expected):
        assert parse_result(result) == expect
