# Guess The Elo Bot

## Purpose

This is a very quick project to strip headers from a chess PGN to anonimise it
for use in a guess the Elo stream.

Currently this is a very quick script that works on a downloaded PGN. Eventual
plans are

1. Turn into a discord bot that can automatically read PGN and
player color from messages in a channel - probably very soon

2. Integration with Lichess and chess.com API to automatically
create studies/analysis boards
    1. Probably gonna happen very quickly with Lichess.
       Not sure about chess.com because so far I cannot find support for it in
       their API. If anyone can help I will appreciate!

3. Remove variations and computer analysis - will take longer than 1.

4. Turn into a full website - only if there's actual requests for it

## Dependencies

Assume `$PYTHON_EXEC` is a replacement for the name of the python executable.
Often this is either `python` or `py` depending on your operating system
(try one or the other till something) works. Please replace `$PYTHON_EXEC` with
the working command and don't actually use `$PYTHON_EXEC` because it doesn't exist.

* [Python 3](https://python.org)
* python-chess
(run in Powershell or terminal: `$PYTHON_EXEC -m pip install python-chess`).

## Usage

### Create file

Create a file for storing which headers you want to keep in the PGN
(I will be using the provided `hdrs.example.txt`)

1. Each header should be on one line
2. For headers that will just be redacted: put just the header name
    1. Ex. WhiteElo
3. For headers that need a custom value: put header and value
separated by an `=`
    1. Ex. Event = Guess The Elo
4. An example header file is in hdrs.txt.example

#### Special headers

There are some special headers

1. SUBMITTER_NAME will be the changed name for who submitted the game
    1. Ex. Game submitter was black, so default behaviour is
       black's name becomes `[Streamer] Sub`
2. OPPONENT_NAME will be the changed name for the opponent
    1. Ex. Game submitter was black, so default behaviour is
        white's name becomes `Random Noob`
3. Any line that starts with a `#` is a comment and is ignored.
You can use this to separate the headers as needed

### Output file extension

Figure out the output file name extension
(ex. if the extension is `_stripped`, then given an input `game.pgn`,
the program will write to `game_stripped.pgn`).
I will call this `output_ext`.

### Running it

Run the actual script. Let's say we are passing in two files: `game1.pgn` and `game2.pgn`
and are using the default hdrs.example.txt provided without modifying it. Assume
the submitters for both games played black.

Open Powershell/terminal, navigate to project directory,
and then run the script. An example command is shown below

```bash
$PYTHON_EXEC strip_headers.py `_stripped` hdrs.example.txt BLACK `game.pgn`
```

### Example Output

`game.pgn` was my example input
`game_stripped.pgn` was my example output

If you have some slight differences, then most likely the project was updated
and this document is out of date. You should still see a usable PGN.

## Finally

Make a Github issue if you have any questions!
