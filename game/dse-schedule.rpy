# The Dating Sim Engine was written by PyTom, 
# with updates added by Andrea Landaker (qirien),
# and contributions by Edmund Wilfong (Pneumonica)
#
# For support, see the Lemma Soft forums thread:
# http://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=31571
#
# It is released under the MIT License - see DSE-LICENSE.txt
#
#
# This is the main part of the program, where you setup your schedule and
# the options for the user. You can change the stats, periods, and choices
# here; just make sure they match up with the events setup in
# dse-events.rpy.  You can even have different time periods (months, instead
# of times of day, for example).

# Set up a default schedule.
init python:
    # Set up attributes here
    register_stat("Strength", "strength", 10, 100)
    register_stat("Agility", "agility", 10, 100)
    register_stat("Endurance", "endurance",10, 100)
    register_stat("Intelligence", "intelligence", 10, 100)
    register_stat("Reaction", "reaction", 10, 100)
    register_stat("Charisma", "charisma", 10, 100)
    register_stat("Perception", "perception", 10, 100)
    register_stat("Appearance", "appearance", 10, 100)
    register_stat("Grades", "grades", 10, 100)

    # Set up Status here
    register_stat("Orientation", "orientation", 50, 100) # 0 = Gay 50 = Bisexual 100 = Straight
    register_stat("Leanings", "leanings", 50, 100) # 0 = Submissive 50 = Neutral 100 = Dominant
    register_stat("Inhibitions", "inhibitions", 75, 100)
    register_stat("Arousal", "arousal", 10, 100)
    register_stat("Pain", "pain", 10, 100)
    register_stat("Health", "health", 10, 100)
    register_stat("Willpower", "health", 10, 100)
    register_stat("Stamina", "stamina", 10, 100)
    register_stat("Mood", "mood", 10, 100)
    register_stat("Sleep", "sleep", 10, 100)

    dp_period("Morning", "morning_act")
    dp_choice("Attend Class", "class")
    dp_choice("Cut Class", "cut")
    
    # This is an example of an event that should only show up under special circumstances
    dp_choice("Fly to the Moon", "fly", show="strength >= 100 and intelligence >= 100")

    dp_period("Afternoon", "afternoon_act")
    dp_choice("Study", "study")
    dp_choice("Hang Out", "hang")

    dp_period("Evening", "evening_act")
    dp_choice("Exercise", "exercise")
    dp_choice("Play Games", "play")

    
# This is the entry point into the game.
label splashscreen:
    scene warning with dissolve
    pause 5.0
    scene logo with dissolve
    pause 5.0
return

label start:

    # Initialize the default values of some of the variables used in
    # the game.
    $ day = 0

    # Show a default background.
    scene black

    # The script here is run before any event.

    "Short."


    # We jump to day to start the first day.
    jump day


# This is the label that is jumped to at the start of a day.
label day:

    # Increment the day it is.
    $ day += 1

    # We may also want to compute the name for the day here, but
    # right now we don't bother.

    "It's day %(day)d."

    # Here, we want to set up some of the default values for the
    # day planner. In a more complicated game, we would probably
    # want to add and remove choices from the dp_ variables
    # (especially dp_period_acts) to reflect the choices the
    # user has available.

    $ morning_act = None
    $ afternoon_act = None
    $ evening_act = None
    $ narrator("What should I do today?", interact=False)
    window show
    

    # Now, we call the day planner, which may set the act variables
    # to new values. We call it with a list of periods that we want
    # to compute the values for.
    call screen day_planner(["Morning", "Afternoon", "Evening"])
    window auto
    
    # We process each of the three periods of the day, in turn.
label morning:

    # Tell the user what period it is.
    centered "Morning"

    # Set these variables to appropriate values, so they can be
    # picked up by the expression in the various events defined below. 
    $ period = "morning"
    $ act = morning_act
    
    # Execute the events for the morning.
    call events_run_period

    # That's it for the morning, so we fall through to the
    # afternoon.

label afternoon:

    # It's possible that we will be skipping the afternoon, if one
    # of the events in the morning jumped to skip_next_period. If
    # so, we should skip the afternoon.
    if check_skip_period():
        jump evening

    # The rest of this is the same as for the morning.

    centered "Afternoon"

    $ period = "afternoon"
    $ act = afternoon_act

    call events_run_period


label evening:
    
    # The evening is the same as the afternoon.
    if check_skip_period():
        jump night

    centered "Evening"

    $ period = "evening"
    $ act = evening_act
    
    call events_run_period


label night:

    # This is now the end of the day, and not a period in which
    # events can be run. We put some boilerplate end-of-day text
    # in here.

    centered "Night"

    "It's getting late, so I decide to go to sleep."

    # We call events_end_day to let it know that the day is done.
    call events_end_day

    # And we jump back to day to start the next day. This goes
    # on forever, until an event ends the game.
    jump day
         

