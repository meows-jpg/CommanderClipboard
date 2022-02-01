"""this is just for testing"""

from main import *


dict = load_commands_json("thisdoesnotexist.json")

for line in dict.items():
    print(line)
