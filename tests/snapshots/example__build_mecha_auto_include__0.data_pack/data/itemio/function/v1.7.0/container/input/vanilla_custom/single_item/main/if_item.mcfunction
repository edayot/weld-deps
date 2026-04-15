
execute store result score #count_input itemio.math.input run data get storage itemio:main.input input.count
execute store result score #count_block itemio.math.input run data get storage itemio:main.input ItemUnique.count

scoreboard players operation #new_count itemio.math.input = #count_block itemio.math.input
scoreboard players operation #new_count itemio.math.input += #count_input itemio.math.input

execute if score #new_count itemio.math.input > #full_stack itemio.math.input run scoreboard players operation #new_count itemio.math.input = #full_stack itemio.math.input

execute if score #new_count itemio.math.input = #count_block itemio.math.input run return fail

data remove storage itemio:main.input Item1
data remove storage itemio:main.input Item2
data modify storage itemio:main.input Item1 set from storage itemio:main.input ItemUnique
data modify storage itemio:main.input Item2 set from storage itemio:main.input input
data remove storage itemio:main.input Item1.count
data remove storage itemio:main.input Item2.count
data remove storage itemio:main.input Item1.Slot
data remove storage itemio:main.input Item2.Slot

execute store success score #!same_item_single itemio.math.input run data modify storage itemio:main.input Item1 set from storage itemio:main.input Item2
execute if score #!same_item_single itemio.math.input matches 1 run return fail

scoreboard players set #success_input itemio.io 1
scoreboard players operation #new_count_input itemio.math.input = #count_input itemio.math.input
scoreboard players operation #new_count_input itemio.math.input += #count_block itemio.math.input
scoreboard players operation #new_count_input itemio.math.input -= #new_count itemio.math.input

execute store result storage itemio:main.input input.count int 1 run scoreboard players get #new_count_input itemio.math.input
execute store result storage itemio:main.input ItemUnique.count int 1 run scoreboard players get #new_count itemio.math.input
