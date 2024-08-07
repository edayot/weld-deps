scoreboard players set @s itemio.math 1
scoreboard players set #if_entity_exist itemio.math 1
scoreboard players operation @s itemio.network_id.low = @e[tag=itemio.cable.me, limit=1] itemio.network_id.low
scoreboard players operation @s itemio.network_id.high = @e[tag=itemio.cable.me, limit=1] itemio.network_id.high
scoreboard players operation @s itemio.network.process_queue = @s itemio.network_id.low
scoreboard players operation @s itemio.network.process_queue %= #process_queue itemio.math
scoreboard players operation #model_final itemio.math = @e[tag=itemio.cable.me, limit=1] itemio.math
function itemio:v1.2.6/servo/calc_cable_model
execute as @e[tag=itemio.cable.me, limit=1] run function itemio:v1.2.6/servo/reload_model
