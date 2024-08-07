execute if score @e[tag=itemio.cable.me, limit=1] itemio.network_id.low matches 1.. run function itemio:v1.2.6/cable/init/regen
execute if score @e[tag=itemio.cable.me, limit=1] itemio.network_id.low matches 0 run function itemio:v1.2.6/cable/init/copy
