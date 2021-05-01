# Discord Bot

## Note

Please quickly read through the first parts of `SCRIPT.md` first.
It has important information.

## Depedencies

You will need the same dependencies as written in `SCRIPT.md`. Please check there
first to make sure you're covered.

Additionally, you will need to run the following command to install the other
dependencies.

`$PYTHON_EXEC -m pip install discord.py python-dotenv`

## Adding the bot to your discord

Before getting started, the bot needs to be added to a server.

Please follow the instructions
[here](https://discordpy.readthedocs.io/en/stable/discord.html)
to create your Discord application and bot.

Make sure you have copied the bot token.

### Private channels

If you are getting your submissions in a private channel, you will need
to invite the bot to this channel once it is in the server.

## Creating environment variables

Firstly, rename or copy the `.env.example` to `.env`.
Then, modify the config values in `.env`, _NOT_ `.env.example`.

Change the `BOT_TOKEN` variable to your bot token.
Then modify any other variables as needed.
All the values are documented in `.env.example`.

## Modifying header file

Modify the headers file (value of `HDR_FILE`) as needed. The documentation for
this can be found in `SCRIPT.md`.

## Testing the bot

Run the script with `$PYTHON_EXEC discord_bot.py`.

## Functionality

Any person in the channel has to submit their game by first typing their color.

For example, let's say someone submitting their game played white.
They first just send a message saying `white` (case doesn't matter).

If there are any other words, or a typo, the message is ignored.

Now there are multiple branches we can go down.

### Valid request

If the message is valid, the bot will tell the submitter to submit their game as
white. The game _HAS_ to be submitted as a file attachment.
It cannot be a simple message.

If the game was parsed successfully, the bot will tell the user this and write
the relevant PGNs (original and stripped) to their respective locations.

### Invalid/Accidental request

If the request was accidental, the original submitter can type `CANCEL`
(case does matter) and the request will be cancelled. This is not strictly
needed because of the timeout, however.

If the game is invalid, the bot will inform the submitter as such.

If there is no `CANCEL` or message with an attachment received in the timeout
period, then the submitter will be informed that they timed out and will have
to start over.

