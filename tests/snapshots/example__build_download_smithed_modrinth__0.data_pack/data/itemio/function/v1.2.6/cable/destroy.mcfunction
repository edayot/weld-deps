tag @s remove itemio.network
tag @s remove itemio.cable.initialised
execute align xyz positioned ~0.5 ~-0.5 ~0.5 as @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run function itemio:v1.2.6/cable/destroy/down
execute align xyz positioned ~0.5 ~1.5 ~0.5 as @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run function itemio:v1.2.6/cable/destroy/up
execute align xyz positioned ~0.5 ~0.5 ~-0.5 as @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run function itemio:v1.2.6/cable/destroy/north
execute align xyz positioned ~0.5 ~0.5 ~1.5 as @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run function itemio:v1.2.6/cable/destroy/south
execute align xyz positioned ~-0.5 ~0.5 ~0.5 as @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run function itemio:v1.2.6/cable/destroy/west
execute align xyz positioned ~1.5 ~0.5 ~0.5 as @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..0.5001, limit=1, sort=nearest] run function itemio:v1.2.6/cable/destroy/east
tag @e[type=#itemio:cables, tag=itemio.network.already_regenerated] remove itemio.network.already_regenerated
execute as @e[type=#itemio:network, tag=itemio.network, tag=!itemio.cable, distance=..0.5001] at @s run function itemio:v1.2.6/cable/destroy/network
execute as @e[type=#itemio:cables, tag=itemio.cable.initialised, distance=..2] at @s run function itemio:v1.2.6/cable/update_model
