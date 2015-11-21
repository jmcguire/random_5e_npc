#!/usr/bin/env python

import web
import yaml
import random_5e_npc

urls = (
  '/', 'index'
)

class index:

  def __init__(self):
    with open("config.yaml") as file:
      self.config = yaml.load(file)
    self.gender = random_5e_npc.picka(self.config['genders'])
    self.race = random_5e_npc.picka(self.config['races'])

  def GET(self):
    return """
<!doctype html>
<html class="no-js" lang="">
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<title>Get a random NPC</title>
<meta name="description" content="">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://reset5.googlecode.com/hg/reset.min.css">
<link href='https://fonts.googleapis.com/css?family=Archivo+Narrow' rel='stylesheet' type='text/css'>
<link href='https://fonts.googleapis.com/css?family=Lobster' rel='stylesheet' type='text/css'>
<!-- design inspired by http://www.twosentencestories.com/ -->
<style>
html {
height: auto;
min-height: 100%%;
}
body{
height: 100%%;
background: #FFF8EF;
background: linear-gradient(to bottom, #FFF8EF 0%%, #CEC3B5 100%%);
}
h1,h2,h3 {
font-family: 'Lobster', Georgia, "Times New Roman", Times, serif;
font-weight: normal;
text-align: center;
margin: 1em auto 0;
}
h1 {
color: #cc4d22;
font-size: 4em;
line-height: 1.3em;
text-shadow: -1px -1px 0 #7F3218;
}
h2 {
color: rgb(183, 112, 89);
font-size: 3em;
text-shadow: -1px -1px 0 #7F3218;
font-style: italic;
margin-top: .5em;
}
h3 {
display: block;
font-size: 2em;
color: #484747;
margin-top: 1.8em;
}
</style>
<h1> %s </h1>
<h2> %s </h2>
<h3> %s </h3>
""" % ( self.name(), self.race_gender(), self.expanded_info() )

  def name(self):
    return "%s" % random_5e_npc.get_a_name(self.gender, self.race, self.config['names'])

  def race_gender(self):
    return "a %s %s" % (self.gender, self.race)

  def expanded_info(self):
    return "(%s, %s/%s, %s)" % (
      random_5e_npc.picka(self.config['classes']),
      random_5e_npc.picka(self.config['align_societies']),
      random_5e_npc.picka(self.config['align_morals']),
      random_5e_npc.picka(self.config['backgrounds']))


if __name__ == "__main__": 

  app = web.application(urls, globals())
  app.run() 

