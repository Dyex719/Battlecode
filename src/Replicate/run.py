
# Running into logical errors :(

import battlecode as bc
import random
import sys
import traceback

print("pystarting")
gc = bc.GameController()
directions = list(bc.Direction)
print("pystarted")

random.seed(8078)
worker_count = 1
knight_count = 0
factory_count = 0

gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()

def factory_logic(unit,knight_count):
    if unit.unit_type == bc.UnitType.Factory:
        garrison = unit.structure_garrison()
        if len(garrison) > 0:
            d = random.choice(directions)
            if gc.can_unload(unit.id, d):
                print('unloaded a knight!')
                gc.unload(unit.id, d)
                return 1
        elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
            gc.produce_robot(unit.id, bc.UnitType.Knight)
            print('produced a knight!')
            knight_count += 1
            return 1
    else:
        print("Recieved non-factory in function")
        return 0

def knight_logic(unit, object_at_distance,location):
    if unit.unit_type == bc.UnitType.Knight:
        d = random.choice(directions)
        try:
            if objects.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, objects.id):
                print('attacked a thing!')
                gc.attack(unit.id, objects.id)
                return 1
            elif objects.team != my_team and gc.is_attack_ready(unit.id):
                shortest_path = unit.location.map_location().direction_to(objects.location.map_location())
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, shortest_path): #can add stuff related to attack cooldown
                    print('Moving towards an enemy')
                    gc.move_robot(unit.id, shortest_path)
                    return 1
            # d = random.choice(directions)
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
                return 0
            else:
                print("knight did nothing")
        except Exception as e:
            print('Error:', e)
            # use this to show where the error was
            traceback.print_exc()
    else:
        print("Recieved non-knight in function")
        return 0

def worker_logic(unit,location):
    d = random.choice(directions)
    # first, let's look for nearby blueprints to work on
    if location.is_on_map():
        nearby = gc.sense_nearby_units(location.map_location(), 2)
        for other in nearby:
            if gc.can_build(unit.id, other.id):
                gc.build(unit.id, other.id)
                print('built a factory!')
                factory_count += 0

    elif gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
         gc.blueprint(unit.id, bc.UnitType.Factory, d)

    # elif gc.can_replicate(unit.id,d):
    #     gc.replicate(unit.id,d)

    elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
        gc.move_robot(unit.id, d)

    else:
        return 0


while True:
    print('pyround:', gc.round())

    try:
        for unit in gc.my_units():
            location = unit.location

            if unit.unit_type == bc.UnitType.Factory:
                return_val = factory_logic(unit)
                if (return_val == 1): continue
            if unit.unit_type == bc.UnitType.Worker:
                return_val = worker_logic(unit,location)
                if (return_val == 1): continue

            units_at_distance = gc.sense_nearby_units(unit.location.map_location(),50)
            for objects in units_at_distance:
                #HARDCODED
                if unit.unit_type == bc.UnitType.Knight:
                    return_val = knight_logic(unit,objects,location)
                    if (return_val == 1): continue

            d = random.choice(directions)

            # the line below gives an ERROR when I use elif CHK
            if (gc.is_move_ready(unit.id) and gc.can_move(unit.id, d)):
                gc.move_robot(unit.id, d)
            else:
                print("Did nothing")

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    gc.next_turn()

    sys.stdout.flush()
    sys.stderr.flush()
