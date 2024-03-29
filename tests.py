import os.path
import sys
import re
from pathlib import Path
import inspect

TEST_MARKER = "is_a_test_function"
EXCLUDE_DIRS = [
    "venv"
]


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
            if not self.should_exclude(path)
        }

    def should_exclude(self, path):
        for ex in EXCLUDE_DIRS:
            if os.path.commonpath([ex, path]) == ex:
                return True
        return False

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

    @test()
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
    def test_theorem_citation(self, line):
        """
        the label for a theorem environment should use text citation
        """
        assert not re.search(r"\\begin{.+}\[\\cite.+\]", line)

    @test(line_based=True)
    def test_paper_mention(self, line):
        """
        should not mention 'paper'
        """
        exceptions = [
            r"\documentclass[a4paper,12pt,oneside]{memoir}",
            "Note that we have changed the notation compared to the original "
            "paper.",
            r"We refer the reader to the original TruthFinder paper"
            r"~\cite{yin2008} for the",
            "describe the axiom in rough terms, deferring to the paper for the"
            " technical",
            r"papers, \textcite{van2011dynamic,van2012evidence,vanbenthem20141"
            "06} made",
        ]
        if line not in exceptions:
            assert "paper" not in line

    @test(line_based=True)
    def test_labelcref(self, line):
        """
        should not use \\labelcref
        """
        assert "\\labelcref" not in line

    @test(line_based=True)
    def test_no_double_quotes(self, line):
        """
        should not use double quotes
        """
        assert '"' not in line

    @test(line_based=True)
    def test_double_quotation(self, line):
        """
        should use double quotation marks
        """
        assert not re.search("[^`]`[^`']+'", line)
        assert not re.search("^`[^`']+'", line)
        assert not re.search("`[^`']+'[^']", line)
        assert not re.search("`[^`']+'$", line)

    @test(line_based=True)
    def test_paragraph_heading_fullstop(self, line):
        """
        paragraph headings should end with a full stop.
        """
        p = r"\paragraph{"
        try:
            idx = line.index(p)
        except ValueError:
            return
        tail = line[(idx + len(p)):]
        contents = ""
        brackets = 0
        for c in tail:
            if c == "{":
                brackets += 1
            elif c == "}":
                brackets -= 1
            if brackets < 0:
                break
            contents += c

        assert contents.endswith(".")

if __name__ == "__main__":
    suite = TestSuite()
    if not suite.run_all():
        sys.exit(1)
