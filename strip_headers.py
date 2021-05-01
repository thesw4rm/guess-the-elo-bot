import chess.pgn
import sys

if len(sys.argv) < 4:
    print("Usage: python " +
          sys.argv[0] + " [output_file_ext] [reqd_headers_file] [submitter_color] [input_files]")
    print("Example: python " +
          sys.argv[0] + " _stripped hdrs.txt BLACK game1.pgn game2.pgn")
    exit(0)

# Will be added to the filename but NOT the file format (ex. if output_ext is "ext" game1.pgn becomes game1_ext.pgn)
output_ext = sys.argv[1].strip() + "."
reqd_headers = {}

# Making sure the case is correct (ex. White and not WHITE)
submitter_color = sys.argv[3].strip().lower().capitalize()


# Verifying color is correct
if not (submitter_color == "White" or submitter_color == "Black"):
    print("ERR - Invalid color of game submitter")
    exit(0)

opponent_color = "Black" if submitter_color == "White" else "White"


def should_ignore_hdr(hdr):
    return hdr is None or hdr.strip() is None or hdr.strip() == "" or hdr.strip()[0] == "#"


with open(sys.argv[2], "r") as hdr_file:
    # Headers separated by a new line, remove spaces at the end
    for hdr in hdr_file:
        # Check if it is a comment or the line is empty
        if should_ignore_hdr(hdr):
            continue
        if "SUBMITTER_NAME" in hdr:
            reqd_headers[submitter_color] = hdr.split("=")[1].strip()
        if "OPPONENT_NAME" in hdr:
            reqd_headers[opponent_color] = hdr.split("=")[1].strip()
        # Check if the header has a constant value
        if "=" in hdr:
            hdr_key, hdr_val = hdr.strip().split("=")[0:2]
            reqd_headers[hdr_key.strip()] = hdr_val.strip()
        # Set it to REDACTED but keep it in there
        else:
            reqd_headers[hdr.strip()] = "REDACTED"

for in_file_name in sys.argv[4:]:
    # rsplit splits by last occurrence of character
    with open(in_file_name, "r") as in_file,  open(output_ext.join(in_file_name.rsplit(".", 1)), "w") as out_file:
        game = chess.pgn.read_game(in_file)
        for hdr in game.headers:
            if hdr in reqd_headers:
                # If we are not keeping the original value
                if reqd_headers[hdr] != "KEEP_ORIG":
                    game.headers[hdr] = reqd_headers[hdr]
            else:
                del game.headers[hdr]
        out_file.write(str(game))
