
execute if block ~ ~ ~ #itemio:container/chests[facing=north] positioned ~1 ~ ~ if block ~ ~ ~ #itemio:container/chests[facing=north, type=right] run function itemio:v1.5.3/container/input/vanilla/double_chest_left/north
execute if block ~ ~ ~ #itemio:container/chests[facing=south] positioned ~-1 ~ ~ if block ~ ~ ~ #itemio:container/chests[facing=south, type=right] run function itemio:v1.5.3/container/input/vanilla/double_chest_left/south

execute if block ~ ~ ~ #itemio:container/chests[facing=west] positioned ~ ~ ~-1 if block ~ ~ ~ #itemio:container/chests[facing=west, type=right] run function itemio:v1.5.3/container/input/vanilla/double_chest_left/west
execute if block ~ ~ ~ #itemio:container/chests[facing=east] positioned ~ ~ ~1 if block ~ ~ ~ #itemio:container/chests[facing=east, type=right] run function itemio:v1.5.3/container/input/vanilla/double_chest_left/east
