# TODO

## General

- Probably don't need to keep defining a total preorder throughout

- Consistency with TD and bipartite tournament chapters:
    - Axiom styling. TD uses uppercase normal text, but tournaments uses bold
      lowercase
    - Use of sectioning. In both we split axioms up according to theme
      (symmetry, independence, monotonicity) but via subsections in TD and
      paragraph headings in tournaments

- Figure out what to do about proof appendices

- Change paper, work etc to chapter, thesis etc

- Change "the appendix" to proper reference

- Proof sketches can be moved out of appendices

- Proofs deferred to the appendix only for space reasons can be moved into the
  body

- Punctuation at the end of display math

- Standardise chapter outlines

- Standardise "conclusion", "summary" section names

- Standardise table formatting

- Standardise \paragraph vs \subsection etc divisions across chapters

- References to `\item`s: I think we have a mix of `\labelcref`, `\cref` and
  custom macros. Similarly for equations

- List proofs: in KR chapter we have references back to items, but not in
  expertise chapter

- Check if `\textcite` is really what I want

- Duplicate references in bibliography

- Shared notation between KR and NMR papers

## TD

- Tikz-ify the figures

## Bipartite tournaments

- Truth discovery reference in the introduction is no longer be appropriate
- There is a commented out table showing axiom satisfaction for the different
  operators. Maybe uncomment it and show it in the text
- Consider using different notation for operators: currently we use φ which
  clashes with the logic part

## Tests

From parsing compile logs:

- Undefined references and citations
- Other errors
- Warnings

# New content

## Extensions and elaborations

- KR paper: more detailed analysis of merging, and compare postulates

## Open questions

- Sums and Monotonicity in TD chapter
- Operator with chain-min, dual and mon simultaneously in tournament chapter
- For expertise models: can closure under arbitrary unions be captured at the
  level of frames?
