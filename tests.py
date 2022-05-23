import sys
import re
from pathlib import Path
import inspect
import functools

TEST_MARKER = "is_a_test_function"


class test:
    def __init__(self, line_based=False):
        self.line_based = line_based

    def __call__(self, test_fn):
        if self.line_based:
            def wrapper(self, lines):
                for i, line in enumerate(lines):
                    try:
                        test_fn(self, line)
                    except AssertionError:
                        assert False, f"line {i + 1}"
            wrapper.__name__ = test_fn.__name__
            wrapper.__doc__ = test_fn.__doc__
            setattr(wrapper, TEST_MARKER, True)
            return wrapper

        setattr(test_fn, TEST_MARKER, True)
        return test_fn


class TestSuite:

    def __init__(self):
        here = Path(__file__).parent
        self.content = {
            str(path): [line.strip() for line in path.read_text().split("\n")]
            for path in here.glob("./**/*.tex")
        }

    def run_all(self):
        tests = inspect.getmembers(self,
                                   predicate=lambda m: hasattr(m, TEST_MARKER))
        passed = True
        for _, test in tests:
            for label, lines in self.content.items():
                try:
                    test(lines)
                except AssertionError as ex:
                    doc = test.__doc__.strip()
                    msg = doc + (f" ({ex})" if str(ex) else "")
                    print(f"{label}: {msg}", file=sys.stderr)
                    passed = False
        return passed

    @test
    def test_blank_line_before_proof(self, lines):
        """
        should not have a blank line before \\end{proof}
        """
        last_was_blank = False
        for i, line in enumerate(lines):
            fail = last_was_blank and "\\end{proof}" in line
            assert not fail, f"line {i + 1}"
            last_was_blank = not line

    @test(line_based=True)
    def test_space_before_footnote(self, line):
        """
        should never have a space before footnotes
        """
        assert not line.startswith("\\footnote{")
        assert not line.startswith("\\footnotemark{")
        assert " \\footnote{" not in line
        assert " \\footnotemark{" not in line

    @test(line_based=True)
    def test_proof_labels(self, line):
        """
        non-default proof labels should start with 'Proof '
        """
        assert not re.search(r"{proof}\[(?!Proof )", line)

    @test(line_based=True)
    def test_paper_mention(self, line):
        """
        should not mention 'paper'
        """
        if "a4paper" not in line:  # exception: options for memoir
            assert "paper" not in line


if __name__ == "__main__":
    suite = TestSuite()
    if not suite.run_all():
        sys.exit(1)
