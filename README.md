# FGC Framework

Hi, I'm CFresh and this is a collection of tools for querying start gg that have been useful to people over the years.

## What is an auth token?

In order to use any of it, you'll need a start gg auth token which you can learn more about [here](https://developer.start.gg/docs/authentication).

If you don't usually use things like this, please know this token is basically your account password, don't send it around.

## Usage

The [releases](https://github.com/SeaFresh/FGC-Framework/releases/tag/v1.0) have the more usable tools set up with a gui, and if you don't know anything about python or using a command line, that's where you'll go.

For the rest of you, StartGGClient has all of the queries and data massaging I do to get things working. Sorry, I know it's a lot.
Everything else is set up as a command line tool with pretty similar options. Many have an @Gooey decorator on their main function. If you find the gui too intrusive, just delete that and you can run it normally. 

## All Seeds

This tool grabs all seeds in order from an event. You've probably seen something like this prior to a major.

## Auto Seeder

This tool seeds a tournament by scoring all players based on the depth they've made it in their last 20 performances for that game.
Obviously this isn't as good as something like ELO or a human touch, but it does pretty well.
The first number it returns is the score, and the second is the number of performances it's based on.
If that second number is low, it means that person hasn't played this game a lot on start gg, so your confidence in their seed should be low.
Sorry if it's a bit slow, it takes about a second per player so that we don't get rate limited.

## Bad Moon Bot

This is something I made for Bad Moon Lee for a joke tournament that I'm not sure if he used.
He was going to randomly DQ someone each round.
It spits out a list of the people still in a bracket.

## Double Bracket

This tool attempts to flag double bracketers in an event by checking if they've entered anything an hour before or after your event.

## Hazard Bots

These tools were (and maybe still are) used by Nick Hazard to run the @NAFGCTO twitter.

## Head to Head

I haven't tested this in a bit. This was intended to try and find 2 players' head to head record to give casters stuff to talk about.

## Loser Bot

This was something Vinny asked for that I think is a lot of fun. It looks over the past X months and tells you how many sets you won, and who beat you in the sets you lost. Good for matchup research.

## Ordered Standings

This is just a way to print out the full standings of an event in order.

## Plisno Bot

Plisno has to seed large tournaments with regulars, and likes to have a slightly more human touch with seeding.
This tool attempts to find other tournaments that your entrants have in common so that you can compare results.
You pass it a number of entrants that are required to be considered in common.

## Set Data

This is something Nick Hazard and I used to pull every single set of GGST once.

## Standings Data

This was another thing we used to pull every set of GGST. It was cool.

## Team Finder

This is something you can use to check what members of an event have a certain prefix. 
Useful if you're not sure who is going to an event from an org.

## Tournament Data

Yet another thing used to pull every set of GGST

## Vinny Bot

This is what Vinny, Sollemnitas, and other staff use to make posts in the Tourney Hub discord.
It looks for tournaments with events starting in the next week for a particular game and formats them for posting in Discord.
Communication in this community is a huge deal to me, it's the reason I made a lot of this stuff because it can be very hard to let people know you're running something. So if you'd like me to add things to, or alter this bot so that you can better inform people about events, let me know.

## Contact Me

I'm most likely to respond here or cfresh on discord.
I'm not sure if I'll open things up to collaborators just yet, I don't really want to manage a big project, but please tell me your bugs, ideas, and ways I can make things more useful to you.