from llmads.cli import run


def test_run():
    assert run('llmad.yaml') == None


if __name__ == '__main__':
    test_run()
