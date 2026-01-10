function #bs.health:add_health with storage lifestring:update
scoreboard players operation @s lifestring.health += #this lifestring.health
execute store result score #max lifestring.health run attribute @s minecraft:max_health get 1000
scoreboard players operation @s lifestring.health < #max lifestring.health
