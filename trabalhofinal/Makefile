all: clean monografia.tex
	pdflatex monografia
	bibtex monografia
	pdflatex monografia
	pdflatex monografia
	evince monografia.pdf&

apre: clean apresentacao.tex
	pdflatex apresentacao.tex
	pdflatex apresentacao.tex
	evince apresentacao.pdf&

clean:
	@rm -f *.pdf *.aux *.toc *.l* *.snm *.out *.nav *.bb* *.bl*
