pdf:
	xelatex -output-directory=.latex main.tex && cp .latex/main.pdf thesis.pdf

print:
	xelatex -output-directory=.latex printedversion.tex && cp .latex/printedversion.pdf printedversion.pdf

bib:
	biber --input-encoding=UTF-8 --output-directory=.latex main

printbib:
	biber --input-encoding=UTF-8 --output-directory=.latex printedversion

test:
	venv/bin/python tests.py && echo "passed"

clean:
	rm .latex/*
