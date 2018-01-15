import battlecode as bc
import random
import sys
import traceback

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)
useful_dir =[]
for x in directions:
    useful_dir.append(x);
tryRotate = [0,-1,1,-2,2]
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

one_loc=None
enemy_start=None

def invert(loc):
    inv_x = earth_map.width-loc.x
    inv_y = earth_map.height-loc.y
    return bc.MapLocation(bc.Planet.Earth,inv_x,inv_y)

# Lets analyse the map
# pm = bc.PlanetMap()
pl = bc.Player(my_team,bc.Planet.Earth)
#for planet in pl.planet: # This is ob wrong, I only want to run the code if it is earth, but it has to run before the main loop starts. We can use a function I guess.
def mid_point(loc1,loc2):
    mid_x = int((loc1.x + loc2.x) / 2)
    mid_y = int((loc1.y + loc2.y) / 2)
    return bc.MapLocation(bc.Planet.Earth,mid_x,mid_y)
#
# def goto(unit,dest):
#     d = unit.location.map_location().direction_to(dest)
#     if gc.can_move(unit.id,d):
#         gc.move_robot(unit.id,d)

def fuzzygoto(gc,tryRotate,directions,unit,dest):
    toward = unit.location.map_location().direction_to(dest)
    for tilt in tryRotate:
        d = rotate(directions,toward,tilt)
        if gc.can_move(unit.id,d):
            gc.move_robot(unit.id,d)
            break

def rotate(directions,direc,amount):
    ind = directions.index(direc)
    return directions[(ind+amount)%8]


while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round())
    
    if(gc.planet()==bc.Planet.Earth and one_loc is None and enemy_start is None):
        earth_map = gc.starting_map(bc.Planet.Earth)
        one_loc = gc.my_units()[0].location.map_location()
        enemy_start = invert(one_loc)
        print("Enemy starts at" + str(enemy_start.x) +" " +str(enemy_start.y))
        print("We start at" + str(one_loc.x) +" " +str(one_loc.y))
        swarm_loc = mid_point(one_loc,enemy_start)
        knight_count = 0    
    
    # frequent try/catches are a good idea
    

    try:
        # walk through our units:
        for unit in gc.my_units():

            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:
                garrison = unit.structure_garrison()
                if len(garrison) > 0:
                    d = random.choice(directions)
                    if gc.can_unload(unit.id, d):
                        print('unloaded a knight!')
                        gc.unload(unit.id, d)
                        continue
                elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                    gc.produce_robot(unit.id, bc.UnitType.Knight)
                    print('produced a knight!')
                    knight_count += 1
                    continue

            # first, let's look for nearby blueprints to work on
            location = unit.location
            if location.is_on_map():
                nearby = gc.sense_nearby_units(location.map_location(), 2)
                for other in nearby:
                    if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
                        gc.build(unit.id, other.id)
                        print('built a factory!')
                        # move onto the next unit
                        continue
                    if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                        print('attacked a thing!')
                        gc.attack(unit.id, other.id)
                        continue
                    elif unit.unit_type == bc.UnitType.Knight and gc.is_move_ready(unit.id) and gc.round()<=150:
                        fuzzygoto(gc,tryRotate,directions,unit,swarm_loc)
                    elif unit.unit_type == bc.UnitType.Knight and gc.is_move_ready(unit.id) and gc.round()>150:
                        fuzzygoto(gc,tryRotate,directions,unit,enemy_start)

            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
            # and if that fails, try to move
           
            #These two statements give an exception. Without these however, the code works just fine
            #elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
             #   gc.move_robot(unit.id,useful_dir)

    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()

