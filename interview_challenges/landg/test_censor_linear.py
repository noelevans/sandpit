import io
import pytest
import time

import censor_serial


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            ("Quick jumped the brown fox", {"jumped", "brown"}),
            "Quick ****** the ***** fox",
        ),
        (
            ("Quick jumped the jumped fox", {"jumped", "brown"}),
            "Quick ****** the ****** fox",
        ),
        (("Quick jumped the brown fox", {}), "Quick jumped the brown fox"),
        (("", ""), ""),
    ],
)
def test_censor_line(test_input, expected):
    prose, banned_words = test_input
    assert expected == "".join(censor_serial.censor_line(banned_words, prose))


def test_run(capfd):
    censor_buffer = io.StringIO("foo\nbar")
    prose_buffer = io.StringIO("aaa foo bbb\naaa bar bbb")
    censor_serial.run(censor_buffer, prose_buffer)
    out, err = capfd.readouterr()
    assert (out).split("\n") == ["aaa *** bbb"] * 2


def test_run_large(capfd):
    n = int(1e6)
    censor_buffer = io.StringIO("foo\nbar")
    prose_buffer = io.StringIO("\n".join(["aaa foo bbb"] * n))
    start = time.time()
    censor_serial.run(censor_buffer, prose_buffer)
    out, err = capfd.readouterr()
    assert time.time() - start < 60
    assert (out).split("\n") == ["aaa *** bbb"] * n
