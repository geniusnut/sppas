## Tokenization

### Overview

Tokenization is also known as "Text Normalization" the process of segmenting a
text into tokens.
In principle, any system that deals with unrestricted text need the text to
be normalized. Texts contain a variety of "non-standard" token types such as
digit sequences, words, acronyms and letter sequences in all capitals, mixed
case words, abbreviations, roman numerals, URL's and e-mail addresses...
Normalizing or rewriting such texts using ordinary words is then an important
issue. The main steps of the text normalization implemented in SPPAS
(Bigi 2011) are:

* Remove punctuation;
* Lower the text;
* Convert numbers to their written form;
* Replace symbols by their written form, thanks to a "replacement" dictionary,
  located into the sub-directory "repl" in the "resources" directory. Do not
  hesitate to add new replacements in this dictionary.
* Word segmentation based on the content of a lexicon. If the
  result is not corresponding to your expectations, fill free to
  modify the lexicon, located in the "vocab" sub-directory of the "resources"
  directory. The lexicon contains one word per line.

### Adapt Tokenization

Word segmentation of SPPAS is mainly based on the use of a lexicon.
If a segmentation is not as expected, it is up to the user to modify
the lexicon. Lexicons of all supported languages are all located in the folder
"vocab" of the "resources" directory. They are in the form of "one
word at a line".

### Perform Tokenization with the GUI

The SPPAS Tokenization system takes as input a file (or a list of files) for
which the name strictly match the name of the audio file except the extension.
For example, if a file with name "oriana1.wav" is given, SPPAS will search for a
file with name "oriana1.xra" at a first stage if ".xra" is set as the default
extension, then it will search for other supported extensions until a file is
found.

This file must include a tier with the orthographic transcription.
At a first stage, SPPAS tries to find a tier with `transcription` as name.
If such a tier does not exist, SPPAS tries to find a tier that contains
one of the following strings:

1. `trans`
2. `trs`
3. `ipu`
4. `ortho`
5. `toe`

The first tier that matches is used (case insensitive search).

Tokenization produces a file with "-tokens" appended to its name,
i.e. "oriana1-tokens.xra" for the previous example.
This file is including only one tier with the resulting tokenization and with
name "Tokenization". In case of an Enriched Orthographic Transcription, to get
both faked and standard tokenized tiers, check the corresponding option. Then,
two tiers will be created:

- "Tokens-std": the text normalization of the standard transcription,
- "Tokens-faked": the text normalization of the faked transcription.

Read the "Introduction" of this chapter for a better understanding of the
difference between "standard" and "faked" transcriptions.

![Text normalization workflow](./etc/figures/tokworkflow.bmp)

To perform the text normalization process, click on the Tokenization activation
button, select the language and click on the "Configure..." blue text to fix
options.


### Perform Tokenization with the CLI

`tokenize.py` is the program to perform Tokenization, i.e. the text
normalization of a given file or a raw text.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
usage: tokenize.py -r vocab [options]

optional arguments:
    -r vocab         Vocabulary file name
    -i file          Input file name
    -o file          Output file name
    --delimiter char Use a delimiter character instead of a space for word delimiter.
    -h, --help       Show the help message and exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following situations are possible:

1. no input is given: the input is `stdin` and the output is `stdout`
(if an output file name is given, it is ignored). In case of Enriched
Orthographic Transcription, only the faked tokenization is printed.

2. an input is given, but no output: the result of the tokenization is
added to the input file.

3. an input and an output are given: the output file is created (or
erased if the file already exists) and the result of the tokenization is
added to this file..


Example of use, using stdin/stdout:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ echo "The te(xt) to normalize 123." |\
  ./sppas/bin/tokenize.py
  -r ./resources/vocab/eng.vocab
$ the te to normalize one_hundred_twenty-three
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In that case, the elision mentionned with the parenthesis is removed
and the number is converted to its written form. The character "_" is
used for compound words (it replaces the whitespace).

Example of use on a transcribed file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ ./sppas/bin/tokenize.py -r ./resources/vocab/eng.vocab
  -i ./samples/samples-eng/oriana1.xra
  -o ./samples/samples-eng/oriana1-token.xra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
