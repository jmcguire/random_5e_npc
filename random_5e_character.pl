#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

my @aligns_1 = qw/Lawful Chaotic Neutral/;
my @aligns_2 = qw/Good Neutral Evil/;
my @classes = qw/Barbarian Fighter Ranger Paladin Monk Bard Rogue Wizard Sorceror Warlock Cleric/;
my @genders = qw/Male Female/;

my %races = (
  Human => ['Calishite', 'Chondathan', 'Damaran', 'Illuskan', 'Mulan', 'Rashemi', 'Shou', 'Tehyrian', 'Turami'],
  Elf => ['High', 'Wood', 'Drow'],
  Dwarf => ['Hill', 'Mountain'],
  Gnome => ['Forest', 'Rock'],
  Halfling => ['Lightfoot', 'Stout'],
  Tiefling => undef,
  Dragonborne => undef,
  'Half-Elf' => undef,
  'Half-Orc' => undef,
);

my %names = (
  ## humans
  Calishite => {
    gender => {
      male => qw/Aseir Bardeid Haseid Khemed Mehmen Sudeiman Zasheir/,
      female => qw/Atala Ceidil Hama Jasmal Meilil Seipora Yasheira Zasheida/,
    },
    last => qw/Basha Dumein Jassan Khalid Mostana Pashar Rein/,
  },
  Chondathan => {
    gender => {
      male => qw/Darvin Dorn Evendur Gorstag Grim Helm Malark Morn Randal Stedd/,
      female => qw/Arveene Esvele Jhessail Kerri Lureene Miri Rowan Shandri Tessele/,
    },
    surname => qw/Amblecrown Buckman Dundragon Evenwood Greycastle Tallstag/
  },
  Damaran => {
    gender => {
      male => qw/Bor Fodel Glar Grigor Igan Ivor Kosef Mival Orel Pavel Sergor/,
      female => qw/Alethra Kara Katernin Mara Natali Olma Tana Zora/,
    },
    surname => qw/Bersk Chernin Dotsk Kulenov Marsk Nemetsk Shemov Starag/
  },
  Illuskan => {
    gender => {
      male => qw/Ander Blath Bran Frath Geth Lander Luth Malcer Stor Taman Urth/,
      female => qw/Amafrey Betha Cefrey Kethra Mara Olga Silifrey Westra/,
    },
    surname => qw/Brightwood Helder Hornraven Lackman Stormwind Windrivver/
  },
  Mulan => {
    gender => {
      male => qw/Aoth Bareris Ehput-Ki Kethoth Mumed Ramas So-Kehur Thazar-De Urhur/,
      female => qw/Arizima Chathi Nephis Nulara Murithi Sefris Thola Umara Zolis/,
    },
    surname => qw/Ankhalab Anskuld Fezim Hahpet Nathandem Sepret Uuthrakt/
  },
   => {
    gender => {
      male => qw//,
      female => qw//,
    },
    surname => qw//
  },
  Shou => {
    gender => {
      male => qw/An Chen Chi Fai Jiang Jun Lian Long Meng On Shan Shui Wen/,
      female => qw/Bai Chao Jia Lei Mei Qiao Shui Tai/,
    },
    surname => qw/Chien Huang Kao Kung Lao Ling Mei Pin Shin Sum Tan Wan/
  },
  Turami => {
    gender => {
      male => qw/Anton Diero Marcon Pieron Rimardo Romero Salazar Umbero/,
      female => qw/Balama Dona Faila Jalana Luisa Marta Quara Selise Vonda/,
    },
    surname => qw/Agosto Astorio Calabra Domine Falone Marivaldi Pisacar Ramondo/
  },

  ## non-humans
  Elf => {
    gender => {
      male => qw/Adran Aelar Aramil Arannis Aust Beiro Berrian Carric  Enialis Erdan Erevan Galinndan Hadarai Heian Himo Immeral Ivellios Laucian Mindartis Paelias Peren Quarion Riardon Rolen Soveliss Thamior Tharivol Theren Varis/,
      female => qw/Adrie Althaea Anastrianna Andraste Antinua Bethrynna Birel Caelynn Drusilia Enna Felosial Ielenia Jelenneth Keyleth Leshanna Lia Meriele Mialee Naivara Quelenna Quillathe Sariel Shanairra Shava Silaqui Theirastra Thia Vadania Valanthe Xanaphia/,
    },
    child => qw/Ara Bryn Del Eryn Faen Innil Lael Mella Naill Naeris Phann Rael Rinn Sai Syllin Thia Vall/,
    family => ('Amakiir (Gemflower)', 'Amastacia (Starflower)', 'Galanodel (Moonwhisper)', 'Holimion (Diamonddew)', 'Ilphelkiir (Gemblossom)', 'Liadon (Silverfrond)', 'Meliamne (Oakenheel)', "Nai'lo (Nightbreeze)", 'Siannodel (Moonbrook)', 'Xiloscient (Goldpetal)',),
  },
  Dwarf => {
    male => qw/Adrik Alberich Baern Barendd Brottor Bruenor Dain Darrak Delg Eberk Einkil Fargrim Flint Gardain Harbek Kildrak Morgran Orsik Oskar Rangrim Rurik Taklinn Thoradin Thorin Tordek Traubon Travok Ulfgar Veit Vondal/,
    female => qw/Amber Artin Audhild Bardryn Dagnal Diesa Eldeth Falkrunn Finellen Gunnloda Gurdis Helja Hlin Kathra Kristryd Ilde Liftrasa Mardred Riswynn Sannl Torbera Torgga Vistra/,
    clan => qw/Balderk Battlehammer Brawnanvil Dankil Fireforge Frostbeard Gorunn Holderhek Ironfist Loderr Lutgehr Rumnaheim Strakeln Torunn Ungart/,
  },
  Gnome => {
    gender => {
      male => qw//,
      female => qw//,
    },
    last => qw//,
  },
  Halfling => {
    gender => {
      male => qw/Alton Ander Cade Corrin Eldon Errich Finnan Garret Lindal Lyle Merric Milo Osborn Perrin Reed Roscoe Wellby/,
      female => qw/Andry Bree Callie Cora Euphemia Jillian Kithri Lavinia Lidda Merla Nedda Paela Portia Seraphina Shaena Trym Vani Verna/,
    },
    family => qw/Brushgather Goodbarrel Greenbottle High-hill Hilltopple Leagallow Tealeaf Thorngage Tosscobble Underbough/,
  },
  Tiefling => {
    gender => {
      male => qw//,
      female => qw//,
    },
    last => qw//,
  },
  Dragonborne => {
    gender => {
      male => qw//,
      female => qw//,
    },
    last => qw//,
  },
  'Half-Elf' => {
    gender => {
      male => qw//,
      female => qw//,
    },
    last => qw//,
  },
  'Half-Orc' => {
    gender => {
      male => qw//,
      female => qw//,
    },
    last => qw//,
  },
);

my @backgrounds = (qw/Acolyte Charlatan Criminal Hermit Noble Outlander Sage Sailor Soldier Urchin/, 'Folk Hero', 'Guild Artisan');

printf "A %s %s, level %d, %s/%s, %s\n"
  ,picka(\%races)
  ,picka(\@classes)
  ,rn(10) + 1
  ,picka(\@aligns_1)
  ,picka(\@aligns_2)
  ,picka(\@backgrounds)
  ;

## give a random number from 0 to <input>
sub rn {
  return rand() * 1000 % shift;
}

## given a list, pick a random element from it
sub picka {
  my $pick = shift;
  return undef unless $pick;
  if ( ref $pick eq 'ARRAY' ) {
    return $pick->[ rn( scalar @$pick ) ];
  } elsif ( ref $pick eq 'HASH' ) {
    my $top_pick = picka([ keys %$pick ]);
    my $sub_pick = picka( $pick->{$top_pick} );
    return $sub_pick ? "$sub_pick $top_pick" : $top_pick;
  } elsif ($pick->[0] =~ /^\d+$/) {
    return rn($pick->[0]) + 1;
  }
}

