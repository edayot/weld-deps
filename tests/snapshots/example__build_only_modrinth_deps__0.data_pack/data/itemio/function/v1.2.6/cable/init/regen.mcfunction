scoreboard players operation #own_network.low itemio.math = @s itemio.network_id.low
scoreboard players operation #own_network.high itemio.math = @s itemio.network_id.high
scoreboard players set #temp_low itemio.math 0
scoreboard players set #temp_high itemio.math 0
scoreboard players operation #temp_low itemio.math = @e[tag=itemio.cable.me, limit=1] itemio.network_id.low
scoreboard players operation #temp_high itemio.math = @e[tag=itemio.cable.me, limit=1] itemio.network_id.high
execute as @e[type=#itemio:network, tag=itemio.network, predicate=itemio:v1.2.6/internal/same_id] run function itemio:v1.2.6/cable/init/gen
