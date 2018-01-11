import battlecode as bc
from battlecode import Location,GameController,PlanetMap
import random
import sys
import traceback

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()
print(gc.karbonite)

while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round())
    # print(PlanetMap.initial_karbonite_at(location()))

    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():
            location = unit.location
            if location.is_on_map():
                if unit.unit_type == bc.UnitType.Worker:

                    # d = random.choice(directions)
                    d = directions[0]
                    # gc.move_robot(unit.id, d)

                    if gc.karbonite_at(location.map_location()) > 0:
                        if gc.can_harvest(unit.id,d) == True:
                             gc.harvest(unit.id,d)
                             print("Amount of Kryptonite left here" + str(gc.karbonite_at(location.map_location())))
                    print("Total karbonite is" + str(gc.karbonite()))

    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    # this is the final yield function.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
