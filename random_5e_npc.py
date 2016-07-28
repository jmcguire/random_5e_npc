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
import sys
import getopt


def picka(picklist):
  """pick a random thing, which could be a range, a list, or a dict"""

  # if it's a dict, we assume it's a hash of lists, then we pick one random
  # key, and then pick on random element from that key's list of items
  # (if it's a hash of hashes, then we'll pretend it's a hash of lists and
  # just pick a key from the inner hash.)
  if (type(picklist) is dict):
    key = random.choice(picklist.keys())
    if type(picklist[key]) is dict:
      # hash of hashes, pretend it's a hash of lists by lookin at the keys
      value = random.choice(picklist[key].keys())
      return "%s %s" % (value, key)
    elif picklist[key]:
      # has of lists
      value = random.choice(picklist[key])
      return "%s %s" % (value, key)
    else:
      # a simple hash, weird!
      return key

  # if it's an array, pick one random element
  elif (type(picklist) is list):
    return random.choice( picklist )

  # if it's a number pick a random number from 1 - picklist
  elif (type(picklist) is int):
    return random.randint(1, picklist)


def get_attributes(attr_array, priority, racial_mods):
  """given a list of 6 attributes, and the priority list, return the abilty score hash"""
  attr_scores = {}
  for i in range(6):
    attr_scores[priority[i]] = attr_array[i]

  # get our races's attribute modifiers
  for attr in racial_mods.keys():
    attr_scores[attr] += racial_mods[attr]

  return attr_scores


def get_racial_mods(race, attribute_mods):
  """given a race and the attribute mod config, return the approp attribute modifiers"""
  if ' Human' in race:
    # all humans subraces are the same, so ignore the subrace
    return attribute_mods['Human']
  elif ' ' in race:
    # subrace exists, meaning there's a subarray
    subrace, primary_race = race.split(' ')
    return attribute_mods[primary_race][subrace]
  else:
    return attribute_mods[race]


def get_a_name(gender, race, name_config):
  """get a name from the complicated name config"""

  # humans are named for their subrace, but all the other races are named for
  # their race
  if ' Human' in race:
    race_name = race.split(' ')[0]
  elif ' ' in race:
    # if the race has a subtype, ignore the subtype
    race_name = race.split(' ')[1]
  else:
    # some races don't have subtypes
    race_name = race

  # each race will different types of names. we're flexible and will get each
  # of them and combine them all
  names_for = name_config[race_name]

  # every race has a gender-based first name
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

def verify_gender(gender, config):
  """check if gender is a valid choice"""
  if gender in config:
    return gender
  else:
    raise ValueError('gender "%s" not found in our list of genders.' % gender)

def verify_class(class_, config):
  """check if class_ is a valid choice"""
  if class_ in config:
    return class_
  else:
    raise ValueError('class "%s" not found in our list of classes.' % class_)

def verify_race(race, config):
  """check if race is a valid choice

  we'll accept three possible types of inputs:
    1) full race name (Hill Dwarf)
    2) only the primary race (Dwarf), and we'll pick a random subrace
    3) only the subrace (Hill), and we'll figure out the primary race
       (this only works because there are no duplicate subrace names)

  we'll do this by building a giant hash with all possible legal values.

  future optimization: cache the non-radom part of this hash, or leave once we
  find a valid choice
  """

  races = {}

  for primary_race in config:
    if config[primary_race] is None:
      # no subraces
      races[primary_race] = primary_race
    else:
      for subrace in config[primary_race]:
        full_race = "%s %s" % (subrace, primary_race)
        races[subrace] = full_race
        races[full_race] = full_race
      # pick a random subrace for this primary race
      races[primary_race] = "%s %s" % (primary_race, picka(config[primary_race]))

  if race in races:
    return races[race]
  else:
    raise ValueError('race "%s" not found in our list of races and subraces.' % race)


if __name__ == '__main__':

  # open config

  with open("pc_config.yaml") as file:
    config = yaml.load(file)

  # parse arguments, all optional

  race = gender = class_ = None

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'r:g:c:', ['race=', 'gender=', 'class='])
  except getopt.GetoptError:
    print "usage: %s (--race <race or subrace>) (--gender <gender>) (--class <class>)"
    sys.exit(2)

  for opt, arg in opts:
    if opt in ('-r', '--race'):
      race = verify_race(arg, config['races'])
    elif opt in ('-g', '--gender'):
      gender = verify_gender(arg, config['genders'])
    elif opt in ('-c', '--class'):
      class_ = verify_class(arg, config['classes'])

  gender = gender or picka(config['genders'])
  race = race or picka(config['races'])
  class_ = class_ or picka(config['classes'].keys())

  # load up our attributes

  attr_score = get_attributes(picka(config['attr_arrays']),
                              config['classes'][class_]['attr_priority'],
                              get_racial_mods(race, config['attribute_mods']))

  attr_string = ', '.join(map(lambda x: "%s: %d" % (x, attr_score[x]), ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']))

  # output result

  print get_a_name(gender, race, config['names'])
  print "%s %s (%s, %s, %s)" % (
    gender,
    race,
    class_,
    picka(config['alignments']),
    picka(config['backgrounds']))
  print attr_string

