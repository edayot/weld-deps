scoreboard players set #double_chests itemio.math 1
scoreboard players set #block_size itemio.math.input 27
function itemio:v1.0.0/container/input/vanilla/try_input
scoreboard players set #double_chests itemio.math 0
execute if score #success_input itemio.io matches 0 positioned ~ ~ ~1 if block ~ ~ ~ chest[facing=west, type=left] run function itemio:v1.0.0/container/input/vanilla/try_input
