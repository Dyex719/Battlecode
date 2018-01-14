import battlecode as bc
import random
import sys
import traceback

# import os
# print(os.getcwd())

print("pystarting")
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

random.seed(8078)

worker_count = 1
knight_count = 0
factory_count = 0


# def worker_priorities(karbonite, worker_count, factory_count, knight_count):
#     if worker_count > knight_count:
#         return 0

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

def knight_logic(unit, object_at_distance):
    if unit.unit_type == bc.UnitType.Knight:
        try:
            if objects.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, objects.id):
                print('attacked a thing!')
                gc.attack(unit.id, objects.id)
                return 1
            elif objects.team != my_team and gc.is_attack_ready(unit.id):
                if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d): #can add stuff related to attack cooldown
                    print('Moving towards an enemy')
                    gc.move_robot(unit.id, unit.location.map_location().direction_to(objects.location.map_location()))
                    return 1
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)
                return 0
        except Exception as e:
            print('Error:', e)
            # use this to show where the error was
            traceback.print_exc()
    else:
        print("Recieved non-knight in function")
        return 0


while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round())

    # frequent try/catches are a good idea
    try:
        # walk through our units:
        for unit in gc.my_units():

            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:

                return_val = factory_logic(unit)
                if (return_val == 0): continue

            # first, let's look for nearby blueprints to work on
            location = unit.location
            if location.is_on_map():
                nearby = gc.sense_nearby_units(location.map_location(), 2)
                for other in nearby:
                    if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
                        gc.build(unit.id, other.id)
                        print('built a factory!')
                        factory_count += 0
                        continue

                units_at_distance = gc.sense_nearby_units(unit.location.map_location(),50)
                for objects in units_at_distance:
                    #HARDCODED
                    if unit.unit_type == bc.UnitType.Knight:
                        return_val = knight_logic(unit,objects)
                        if (return_val == 0): continue

            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
            # and if that fails, try to move
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)

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
