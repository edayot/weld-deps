execute if entity @s[tag=!itemio.container.not_vanilla_container] run function itemio:v1.0.0/container/disabling_hopper
scoreboard players add @s itemio.minecart_check 0
execute if entity @s[scores={itemio.minecart_check=1..}, tag=!itemio.container.not_vanilla_container] positioned ~ ~-1 ~ as @e[type=hopper_minecart, distance=..1.5, tag=!itemio.minecart_disabled] run function itemio:v1.0.0/container/disable_minecart
scoreboard players remove @s itemio.minecart_check 1
execute if entity @s[tag=itemio.container.hopper] if predicate itemio:v1.0.0/internal/good_queue_container run function itemio:v1.0.0/container/8tick
