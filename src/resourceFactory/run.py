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

my_team = gc.team()
print(gc.karbonite)

while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round())
    # print(PlanetMap.initial_karbonite_at(location()))

    try:
        for unit in gc.my_units():
            if unit.unit_type == bc.UnitType.Worker:
                location = unit.location

                if location.is_on_map(): #could be in space
                    nearby = gc.sense_nearby_units(location.map_location(),2)
                    for other in nearby:
                        if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id) and other.structure_is_built:
                            gc.build(unit.id, other.id)
                            print('built a factory!')
                            continue

                d = random.choice(directions)

                if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                    gc.blueprint(unit.id, bc.UnitType.Factory, d)


                elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                    map_location = (unit.location).map_location()
                    surr=gc.all_locations_within(map_location,9)
                    moves=[]
                    for loc in surr:
                        if(gc.karbonite_at(loc)>0):
                            moves.append(map_location.direction_to(loc))
                    move=random.choice(moves)
                    movePoss=gc.is_move_ready(unit.id)
                    moveOcc=gc.is_occupiable(map_location.add(move))
                    if(movePoss and moveOcc):
                        gc.move_robot(unit.id,move)
                    print(gc.karbonite())


                else:
                    print("does nothing")

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()



    # send the actions we've performed, and wait for our next turn.
    # this is the final yield function.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
