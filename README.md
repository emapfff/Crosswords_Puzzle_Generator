# Crossword Generation
By using an evolutionary algorithm (EA), I wrote code based on Evaluation algorithm, which include crossover and mutation functions for evolving crosswords.
## Desctription:
### Input format:
- Z ∈ [5; 20] words of length
- N ∈ [2; 20] separated by new lines.
- The inputs are guaranteed to be giving at least 1 valid solution.
### Output format:
The output should contain Z lines, corresponding to each input word. Each line should
contain 3 integers:
- Crossword’s row number X of the word’s first symbol (� ∈ [0; 19])
- Crossword’s column number Y of the word’s first symbol (� ∈ [0; 19])
- Horizontal (0) or Vertical (1) location
