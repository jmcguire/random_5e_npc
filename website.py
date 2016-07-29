#!/usr/bin/env python

import web
import yaml
import random_5e_npc

urls = (
  '/', 'index'
)

class index:

  def __init__(self):
    with open("pc_config.yaml") as file:
      self.config = yaml.load(file)
    self.gender = random_5e_npc.picka(self.config['genders'])
    self.race = random_5e_npc.picka(self.config['races'])
    self.class_ = random_5e_npc.picka(self.config['classes'].keys())

    self.name = random_5e_npc.get_a_name(self.gender, self.race, self.config['names'])
    self.alignment = random_5e_npc.picka(self.config['alignments'])
    self.background = random_5e_npc.picka(self.config['backgrounds'])

    self.attr_score = random_5e_npc.get_attributes(random_5e_npc.picka(self.config['attr_arrays']),
                                                   self.config['classes'][self.class_]['attr_priority'],
                                                   random_5e_npc.get_racial_mods(self.race, self.config['attribute_mods']))
    self.attr_string = ', '.join(map(lambda x: "<b>%s:</b> %d" % (x, self.attr_score[x]), ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']))



  def GET(self):
    return """
<!doctype html>
<html class="no-js" lang="en">
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<title>Create a random and well-named NPC for D&D 5e</title>
<meta name="description" content="Refresh to get a well-named NPC, using names from the 5th Edition Players Handbook">
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
<h2> %s %s (%s, %s, %s) </h2>
<h3> %s </h3>
<script>
(function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
e=o.createElement(i);r=o.getElementsByTagName(i)[0];
e.src='https://www.google-analytics.com/analytics.js';
r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
ga('create','UA-42761539-2','auto');ga('send','pageview');
</script>
<!-- by Justin McGuire, jm@landedstar.com, @landedstar  -->
<!-- https://github.com/jmcguire/random_5e_npc -->
""" % (self.name,
       self.gender, self.race, self.class_, self.alignment, self.background,
       self.attr_string)


if __name__ == "__main__": 

  app = web.application(urls, globals())
  app.run() 

