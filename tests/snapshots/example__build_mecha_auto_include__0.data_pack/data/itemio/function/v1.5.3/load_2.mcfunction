
forceload add -30000000 1600

execute if loaded -30000000 20 1610 run function itemio:v1.5.3/placing_worldborder_things

scoreboard players set #loaded itemio.math 0
execute as a97c9c67-fde0-4b89-926d-54fa4a866004 if entity @s as a97c9c67-fde0-4b89-926d-54fa4a866004 if entity @s run scoreboard players set #loaded itemio.math 1

execute if score #loaded itemio.math matches 0 run forceload add -30000000 1600
execute if score #loaded itemio.math matches 0 run schedule function itemio:v1.5.3/load_2 5 replace

execute if score #loaded itemio.math matches 1 run function itemio:v1.5.3/load_4
