pdf:
	pdflatex -output-directory=.latex main.tex && cp .latex/main.pdf thesis.pdf

bib:
	biber --output-directory=.latex main
