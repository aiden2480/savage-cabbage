from setup import CMDS, CMD_CLASSES
import random
cmd, args= "help", [random.choice(list(CMDS.keys()) + CMD_CLASSES + ['lol', 'poop', 'noob', 'no u', 'wet bread gamers'])]

if cmd == 'help': # Double indent for compatibility for when I add to main
        print(args[0])
        if args[0] not in list(CMDS.keys()) + CMD_CLASSES:
            print("lol thats not a command!")
        else:
            args = [arg.lower() for arg in args]
            if args[0] in list(CMDS.keys()): # Command
                print(CMDS[args[0]][0])
                print(f"Aliases: {}")"
            else: # Class
                pass