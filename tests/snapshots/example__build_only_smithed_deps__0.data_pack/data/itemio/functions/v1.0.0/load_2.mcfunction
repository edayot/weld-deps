forceload add -30000000 1600
execute if loaded -30000000 20 1610 run function itemio:v1.0.0/placing_worldborder_things
scoreboard players set #loaded itemio.math 0
execute as 93682a08-d099-4e8f-a4a6-1e33a3692301 if entity @s run scoreboard players set #loaded itemio.math 1
execute if score #loaded itemio.math matches 0 run forceload add -30000000 1600
execute if score #loaded itemio.math matches 0 run schedule function itemio:v1.0.0/load_2 5 replace
execute if score #loaded itemio.math matches 1 run function itemio:v1.0.0/load_4
