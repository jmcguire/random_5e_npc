#!/usr/bin/env python
"""
random_5e_npc.py

Generate a simple character for D&D 5e.  It will produce an appropriate
name based o random race and gender.  All the names are copied from the
Players Handbook.  It also adds a random class, alignment, and
background.

Created by Justin McGuire <jm@landedstar.com>
Content copyright Wizards of the Coast
"""

import yaml
import random

def main():
  with open("config.yaml") as file:
    config = yaml.load(file)

  gender = picka(config['genders'])
  race = picka(config['races'])

  print "%s, a %s %s (%s, %s/%s, %s)" % (
    get_a_name(gender, race, config['names']),
    gender,
    race,
    picka(config['classes']),
    picka(config['align_societies']),
    picka(config['align_morals']),
    picka(config['backgrounds']))


def picka(picklist):
  """pick a random thing, which could be a range, a list, or a dict"""

  ## if it's a dict, we assume it's a hash of lists, then we pick one random
  ## key, and then pick on random element from that key's list of items
  if (type(picklist) is dict):
    key = random.choice(picklist.keys())
    if picklist[key]:
      value = random.choice(picklist[key])
      return "%s %s" % (value, key)
    else:
      return key

  ## if it's an array, pick one random element
  elif (type(picklist) is list):
    return random.choice( picklist )

  ## if it's a number pick a random number from 1 - picklist
  elif (type(picklist) is int):
    return random.randint(1, picklist)


def get_a_name(gender, race, name_config):
  """get a name from the complicated name config"""

  ## humans are named for their subrace, but all the other races are named for
  ## their race
  if ' Human' in race:
    race_name = race.split(' ')[0]
  elif ' ' in race:
    ## if the race has a subtype, ignore the subtype
    race_name = race.split(' ')[1]
  else:
    ## some races don't have subtypes
    race_name = race

  ## each race will different types of names. we're flexible and will get each
  ## of them and combine them all
  names_for = name_config[race_name]

  ## every race has a gender-based first name
  name = picka(names_for['gender'][gender])

  if 'surname' in names_for:
    name += ' ' + picka(names_for['surname'])

  for name_type in ['family', 'clan', 'virtue']:
    if name_type in names_for:
      name += ' of the ' + picka(names_for[name_type]) + ' ' + name_type.title()

  if 'child' in names_for:
    name += ', named ' + picka(names_for['child']) + ' as a child'

  if 'nickname' in names_for:
    name += ', nicknamed ' + picka(names_for['nickname'])

  return name


if __name__ == '__main__':
  main()

