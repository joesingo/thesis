pdf:
	xelatex -output-directory=.latex main.tex && cp .latex/main.pdf thesis.pdf

bib:
	biber --input-encoding=UTF-8 --output-directory=.latex main

test:
	venv/bin/python tests.py && echo "passed"

clean:
	rm .latex/*
