scoreboard players set #model_final itemio.math 0
execute align xyz positioned ~0.5 ~-0.5 ~0.5 if entity @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run scoreboard players add #model_final itemio.math 2
execute align xyz positioned ~0.5 ~1.5 ~0.5 if entity @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run scoreboard players add #model_final itemio.math 1
execute align xyz positioned ~0.5 ~0.5 ~-0.5 if entity @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run scoreboard players add #model_final itemio.math 4
execute align xyz positioned ~0.5 ~0.5 ~1.5 if entity @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run scoreboard players add #model_final itemio.math 8
execute align xyz positioned ~-0.5 ~0.5 ~0.5 if entity @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run scoreboard players add #model_final itemio.math 16
execute align xyz positioned ~1.5 ~0.5 ~0.5 if entity @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run scoreboard players add #model_final itemio.math 32
execute align xyz positioned ~0.5 ~0.5 ~0.5 as @e[type=#itemio:network, tag=itemio.network, tag=!itemio.cable, distance=..0.5001] run function itemio:v1.2.6/servo/calc_cable_model
scoreboard players set @s itemio.math 0
scoreboard players operation @s itemio.math = #model_final itemio.math
function #itemio:event/cable_update
