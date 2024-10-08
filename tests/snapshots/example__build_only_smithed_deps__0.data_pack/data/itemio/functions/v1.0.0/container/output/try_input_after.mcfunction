scoreboard players set #success_input itemio.io 0
execute as @e[tag=itemio.transfer.destination, tag=!itemio.transfer.destination.already] unless entity @s[distance=..0.5001] run tag @s add itemio.transfer.destination.good_distance
execute as @e[tag=itemio.transfer.destination.good_distance, limit=1, sort=nearest] at @s run function itemio:v1.0.0/container/output/try_input_after/loop
tag @e[tag=itemio.transfer.destination.already] remove itemio.transfer.destination.already
tag @e[tag=itemio.transfer.destination.good_distance] remove itemio.transfer.destination.good_distance
execute if score #success_input itemio.io matches 1 run scoreboard players operation #remove_count itemio.math.output = #count_to_remove itemio.io
execute if score #success_input itemio.io matches 0 run scoreboard players set #remove_count itemio.math.output 0
execute if score #servos_transfer itemio.math matches 1 if score #success_input itemio.io matches 0 run function #itemio:calls/disable_servo
