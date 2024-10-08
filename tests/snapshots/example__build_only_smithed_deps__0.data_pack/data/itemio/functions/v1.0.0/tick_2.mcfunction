execute at @e[type=hopper_minecart] positioned ~ ~1 ~ run scoreboard players set @e[type=#itemio:container, tag=itemio.container.initialised, scores={itemio.minecart_check=..1}] itemio.minecart_check 5
execute as @e[type=#itemio:container, tag=itemio.container.initialised] at @s run function itemio:v1.0.0/container/tick
execute as @e[type=hopper_minecart, tag=itemio.minecart_disabled] at @s run function itemio:v1.0.0/container/disable_minecart
execute as @e[type=#itemio:servos, tag=itemio.servo.extract, tag=itemio.servo.initialised, predicate=itemio:v1.0.0/internal/good_queue] run function itemio:v1.0.0/servo/test_already
tag @e[tag=itemio.servo.already] remove itemio.servo.already
scoreboard players remove @e[type=#itemio:servos, tag=itemio.servo.initialised, scores={itemio.servo.cooldown=1..}] itemio.servo.cooldown 1
execute if score #current_queue itemio.math matches ..0 run scoreboard players operation #current_queue itemio.math = #process_queue itemio.math
scoreboard players remove #current_queue itemio.math 1
execute if score #current_queue_container itemio.math matches ..0 run scoreboard players operation #current_queue_container itemio.math = #hopper_speed itemio.math
scoreboard players remove #current_queue_container itemio.math 1
