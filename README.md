# Guess The Elo Bot

## Purpose

This is a project to strip headers from a chess PGN to anonimise it
for use in a guess the Elo stream.

Eventual plans are

1. ~~Turn into a discord bot that can automatically read PGN and
player color from messages in a channel~~ - DONE

2. Integration with Lichess and chess.com API to automatically
create studies/analysis boards
    1. Probably gonna happen very quickly with Lichess.
       Not sure about chess.com because so far I cannot find support for it in
       their API. If anyone can help I will appreciate!

3. Remove variations and computer analysis - will take a while

4. Turn into a full website - only if there's actual requests for it

## Documentation

To strip headers from individual PGN files, please see `SCRIPT.md`.

To create a discord bot that creates original and stripped PGN files from
messages in a channel, please see `DISCORD_BOT.md`.
Please don't forget to rename `.env.example` to `.env` and modify the values
as per your needs.


