pdf:
	xelatex -output-directory=.latex main.tex && cp .latex/main.pdf thesis.pdf

bib:
	biber --input-encoding=UTF-8 --output-directory=.latex main

test:
	venv/bin/python tests.py && echo "passed"

mkdict:
	~/coding/apps/nvim/nvim.appimage -Es -c "set spell" -c "spelldump" \
		-c "write /tmp/dict" || true
	cat /tmp/dict \
		| sed 's,/.*,,' \
		| grep -v "^#" \
		| aspell --lang=en create master ./.dict

spell:
	cat chapters/**/*.tex | \
	aspell \
		--master=./.dict \
		--mode=tex \
		--add-tex-command="cref op" \
		--add-tex-command="Cref op" \
		--add-tex-command="cite op" \
		--add-tex-command="textcite op" \
		--add-tex-command="array op" \
		--add-tex-command="label op" \
		--add-tex-command="node op" \
		--add-tex-command="draw op" \
		--add-tex-command="color op" \
		--add-tex-command="tabular op" \
		list \
		| sort | uniq

clean:
	rm .latex/*
