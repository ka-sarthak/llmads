from llmads.cli import parse


def test_parse():
    assert parse('llmad.yaml') == None


if __name__ == '__main__':
    test_parse()
