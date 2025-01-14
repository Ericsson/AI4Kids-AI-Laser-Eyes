class USED_LANGUAGE(object):
    laser_eyes_string = "Laser Eyes !"
    bottle_touched_string = 'Bottles touched: {}'
    timer_string = 'Timer: {:.1f}'
    play_string = 'Play'


class FRENCH_LANGUAGE(object):
    laser_eyes_string = "Yeux Laser !"
    bottle_touched_string = 'Bouteilles touchées: {}'
    timer_string = 'Temps: {:.1f}'
    play_string = 'Jouer'


class ENGLISH_LANGUAGE(object):
    laser_eyes_string = "Laser Eyes !"
    bottle_touched_string = 'Bottles touched: {}'
    timer_string = 'Timer: {:.1f}'
    play_string = 'Play'


def change_language(USED_LANGUAGE, NEW_LANGUAGE):
    USED_LANGUAGE.laser_eyes_string = NEW_LANGUAGE.laser_eyes_string
    USED_LANGUAGE.bottle_touched_string = NEW_LANGUAGE.bottle_touched_string
    USED_LANGUAGE.timer_string = NEW_LANGUAGE.timer_string
    USED_LANGUAGE.play_string = NEW_LANGUAGE.play_string
