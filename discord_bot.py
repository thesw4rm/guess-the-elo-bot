import chess.pgn
import io
import sys
import discord
import os
import asyncio
from dotenv import dotenv_values
import uuid

config = dotenv_values(".env")  # Config values loaded from .env file

BOT_TOKEN = config["BOT_TOKEN"]
HDR_FILE = config["HDR_FILE"]
CHAN_NAME = config["CHANNEL_NAME"]
OUTPUT_FILE_EXT = config["OUTPUT_FILE_EXT"]
ORIG_FILE_DIR = config["ORIG_FILE_DIR"]
STRIPPED_FILE_DIR = config["STRIPPED_FILE_DIR"]
GAME_TIMEOUT = float(config["GAME_TIMEOUT"])


reqd_headers = {}


def should_ignore_hdr(hdr):
    return hdr is None or hdr.strip() is None or hdr.strip() == "" or hdr.strip()[0] == "#"


with open(HDR_FILE, "r") as hdr_file:
    # Headers separated by a new line, remove spaces at the end
    for hdr in hdr_file:
        # Remove comments
        hdr = hdr.split("#")[0]
        # Check if it is a comment or the line is empty
        if should_ignore_hdr(hdr):
            continue

        if "SUBMITTER_NAME" in hdr:
            reqd_headers["_SUB_NAME"] = hdr.split("=")[1].strip()

        if "OPPONENT_NAME" in hdr:
            reqd_headers["_OP_NAME"] = hdr.split("=")[1].strip()

        # Check if the header has a constant value
        if "=" in hdr:
            hdr_key, hdr_val = hdr.strip().split("=")[0:2]
            reqd_headers[hdr_key.strip()] = hdr_val.strip()

        # Set it to REDACTED but keep it in there
        else:
            reqd_headers[hdr.strip()] = "REDACTED"

# Starting the discord bot
client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as {0.user}. Ready to receive games.".format(client))


# Verify either cancel or the game was processed properly
def verify_received_pgn(msg):
    # Game must be attached as file.
    # Copy pasted games are not allowed as of the moment
    return msg.content == "CANCEL" or len(msg.attachments) > 0


@client.event
async def on_message(msg):

    # If this is a bot message
    if msg.author == client.user or msg.channel.name != CHAN_NAME:
        return

    # Checking if this is a game or a typo/general discussion
    if msg.content.lower() == "white" or msg.content.lower() == "black":
        await msg.channel.send(msg.author.mention)
        await msg.channel.send("I understand you "
                               "played {.content} in your game. Please copy paste your whole PGN and nothing else, "
                               "or type CANCEL to start over.".format(msg))
    else:
        return

    if msg.content.lower() == "white":
        sub_color = "White"
        op_color = "Black"
    else:
        sub_color = "Black"
        op_color = "White"

    # Waiting max 10 seconds for a PGN to be pasted
    try:
        msg = await client.wait_for('message',
                                    check=verify_received_pgn,
                                    timeout=GAME_TIMEOUT)
    except asyncio.TimeoutError:
        await msg.channel.send("{.author} You took too long to send a"
                               "pgn. Please try again.".format(msg))
        return

    if msg:
        if len(msg.attachments) == 0 and msg.content == "CANCEL":
            await msg.channel.send("{.author} Cancellation "
                                   "received.".format(msg))
            return
        orig_game = await msg.attachments[0].read()
        str_io = io.StringIO(orig_game.decode("utf-8"))

        try:
            game = chess.pgn.read_game(str_io)
        except ValueError:
            return await msg.channel.send("{.author} Failure parsing"
                                          "pgn".format(msg))

        for hdr in game.headers:
            if hdr in reqd_headers:
                # If we are not keeping the original value
                if reqd_headers[hdr] != "KEEP_ORIG":
                    game.headers[hdr] = reqd_headers[hdr]
            else:
                del game.headers[hdr]

        # Special headers come last so that the above for loop
        # doesn't override them
        game.headers[sub_color] = reqd_headers["_SUB_NAME"]
        game.headers[op_color] = reqd_headers["_OP_NAME"]
        stripped_game = str(game)

        if "?" in stripped_game:
            return await msg.channel.send("{.author} Failure parsing"
                                          "PGN.".format(msg))
        await msg.channel.send("{.author} Successfully imported your"
                               "PGN!".format(msg))

        # UUID will generate a different filename for each game
        file_id = str(uuid.uuid1())

        # Writing the original game
        with open(ORIG_FILE_DIR + file_id + ".pgn", "w") as orig_file:
            orig_file.write(orig_game.decode("utf-8"))

        # Writing the stripped/anonimised game
        with open(STRIPPED_FILE_DIR + file_id + OUTPUT_FILE_EXT + ".pgn", "w") as stripped_file:
            stripped_file.write(stripped_game)


client.run(BOT_TOKEN)
