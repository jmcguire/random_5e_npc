#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use YAML::XS 'LoadFile';

##
## MAIN
##

my $config = LoadFile("config.yaml");

my $gender = picka($config->{genders});
my $race = picka($config->{races});

printf "%s, a %s %s %s, %s/%s, %s\n"
  ,get_a_name($race, $gender, $config->{names})
  ,$gender
  ,$race
  ,picka($config->{classes})
  ,picka($config->{align_societies})
  ,picka($config->{align_morals})
  ,picka($config->{backgrounds})
  ;

exit;

##
## SUBROUTINES
##

## return a random number from 0 to <input>
sub rn {
  return rand() * 1000 % shift;
}

## pick a random thing from a list
sub picka {
  my $pick = shift;
  return undef unless $pick;

  ## if it's an array, pick one random element
  if ( ref $pick eq 'ARRAY' ) {
    return $pick->[ rn( scalar @$pick ) ];

  ## if it's a hash, we assume it's a has of lists, then we pick one random
  ## key, and then pick on random element from that key's list of items
  } elsif ( ref $pick eq 'HASH' ) {
    my $top_pick = picka([ keys %$pick ]);
    my $sub_pick = picka( $pick->{$top_pick} );
    return $sub_pick ? "$sub_pick $top_pick" : $top_pick;

  ## if it's a number pick a random number from 1 - $pick
  } elsif ($pick->[0] =~ /^\d+$/) {
    return rn($pick->[0]) + 1;
  }

}

## get a name from the complicated name config
sub get_a_name {
  my ($race, $gender, $name_config) = @_;

  ## humans are named for their subrace, but all the other races are named for
  ## their race
  my $race_name;
  if ($race =~ ' Human') {
    ($race_name) = $race =~ /^([\w-]+) Human$/;
  } elsif ($race =~ / /) {
    ## if the race has a subtype, ignore it
    ($race_name) = $race =~ / ([\w-]+)$/;
  } else {
    ## some races don't have subtypes
    $race_name = $race;
  }

  ## each race will different types of names. we're flexible and will get each
  ## of them and combine them all
  my $names_for = $name_config->{$race_name};
  my @name_types = keys %$names_for;

  ## start with the first name
  my $name = picka($names_for->{gender}->{$gender});

  ## then get the last name
  if ($names_for->{last}) {
    $name .= ' ' . picka($names_for->{last});
  }
  if ($names_for->{surname}) {
    $name .= ' ' . picka($names_for->{surname});
  }

  ## finally assmemble the other names
  foreach my $name_type (@name_types) {
    next if $name_type eq 'gender';
    next if $name_type eq 'last';
    next if $name_type eq 'surname';
    next if $name_type eq 'child';
    next if $name_type eq 'nickname';
    $name .= ' of the ' . (ucfirst $name_type) . ' ' . picka($names_for->{$name_type});
  }

  ## add on the weird "child" name
  if ($names_for->{child}) {
    $name .= ', named ' . picka($names_for->{child}) . ' as a child';
  }

  ## add on the nickname
  if ($names_for->{nickname}) {
    $name .= ', nicknamed ' . picka($names_for->{nickname});
  }

  return "$name";
}

