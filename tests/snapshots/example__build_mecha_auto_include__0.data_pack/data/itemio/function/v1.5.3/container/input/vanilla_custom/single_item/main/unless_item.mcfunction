
execute store result score #count_input itemio.math.input run data get storage itemio:main.input input.count

scoreboard players operation #new_count itemio.math.input = #count_input itemio.math.input

execute if score #new_count itemio.math.input > #full_stack itemio.math.input run scoreboard players operation #new_count itemio.math.input = #full_stack itemio.math.input

scoreboard players set #success_input itemio.io 1
scoreboard players operation #new_count_input itemio.math.input = #count_input itemio.math.input
scoreboard players operation #new_count_input itemio.math.input -= #new_count itemio.math.input

execute store result storage itemio:main.input input.count int 1 run scoreboard players get #new_count_input itemio.math.input
data remove storage itemio:main.input ItemUnique
data modify storage itemio:main.input ItemUnique set from storage itemio:main.input input
execute store result storage itemio:main.input ItemUnique.count int 1 run scoreboard players get #new_count itemio.math.input
