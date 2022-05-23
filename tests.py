import sys
from pathlib import Path
import inspect

TEST_MARKER = "is_a_test_function"


def test(test_fn):
    setattr(test_fn, TEST_MARKER, True)
    return test_fn


class TestSuite:

    def __init__(self):
        here = Path(__file__).parent
        self.content = {
            str(path): path.read_text().split("\n")
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
            line = line.strip()
            if last_was_blank and "\\end{proof}" in line:
                assert False, f"line {i + 1}"
            last_was_blank = not line


if __name__ == "__main__":
    suite = TestSuite()
    if not suite.run_all():
        sys.exit(1)
