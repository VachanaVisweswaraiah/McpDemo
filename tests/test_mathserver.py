from conftest import load_module

mathserver = load_module("mathserver_under_test", "03_mcplangchain/mathserver.py")


def test_add_returns_sum():
    assert mathserver.add(3, 5) == 8


def test_multiple_returns_product():
    assert mathserver.multiple(8, 12) == 96
