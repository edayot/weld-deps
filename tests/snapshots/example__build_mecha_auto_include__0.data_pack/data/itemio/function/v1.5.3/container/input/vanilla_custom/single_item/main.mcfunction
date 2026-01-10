
data remove storage itemio:main.input input
data modify storage itemio:main.input input set from storage itemio:io input

execute store result score #if_item itemio.math.input if data storage itemio:main.input ItemUnique

scoreboard players set #full_stack itemio.math.input 64
data remove storage itemio:main get_stack_size
data modify storage itemio:main get_stack_size set from storage itemio:main.input input
execute store result score #full_stack itemio.math.input run function itemio:v1.5.3/utils/get_stack_size
execute if score #override_stack_size itemio.math.input matches 1 run scoreboard players set #full_stack itemio.math.input 1

execute if score #if_item itemio.math.input matches 1 run function itemio:v1.5.3/container/input/vanilla_custom/single_item/main/if_item

execute if score #if_item itemio.math.input matches 0 run function itemio:v1.5.3/container/input/vanilla_custom/single_item/main/unless_item

data remove storage itemio:io output
data modify storage itemio:io output set from storage itemio:io input
data modify storage itemio:io output.count set from storage itemio:main.input input.count

execute store result score #count_input itemio.math.input run data get storage itemio:io input.count
execute store result score #count_output itemio.math.input run data get storage itemio:io output.count

scoreboard players set #count_to_remove itemio.math.input 0
scoreboard players operation #count_to_remove itemio.math.input = #count_input itemio.math.input
scoreboard players operation #count_to_remove itemio.math.input -= #count_output itemio.math.input

scoreboard players operation #count_to_remove itemio.io = #count_to_remove itemio.math.input
