### Roblox Moderation for Gooners

This tool is based off the program shown in RubenSim's latest video, ["Fighting Roblox's Gooning Crisis,"](https://www.youtube.com/watch?v=oB_TZ8lFe18) which takes in a list of ROBLOX group IDs, gets their users and checks for common groups between these users.

While RubenSim does show the results of running the code and the first few lines of the program near the middle and end of his video, I wanted to test my mettle as well as uncover how this worked and thus made my own program replicating his.

The primary different that you will see here is that I do not implement concurrency in the program, resulting in slower runtimes. This is something I will need to work on as I am not yet familar with those concepts.

### How to Moderate for Dummies

1. Open up `main.py` in your IDE or text editor of choice.
2. Head to the beginning of the `__main__` if statement.
3. In here, you will see several variables that you can tinker with. The most important one will be `group_ids`, which holds the IDs of the groups you want to check.
4. Once you have modified these values to your liking, execute `main.py` and enjoy!