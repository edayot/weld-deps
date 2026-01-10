
execute store result storage itemio:main.input input.count int 1 run scoreboard players get #full_stack itemio.math.input
execute if score #nbt_items itemio.math.input matches 0 run data modify block ~ ~ ~ Items append from storage itemio:main.input input
execute if score #nbt_items itemio.math.input matches 1 run function itemio:v1.5.3/container/input/custom/input_no_config/process_input/unless_item/sup/nbt_items with storage itemio:main.input temp.args

scoreboard players operation #new_count_input itemio.math.input = #count_input itemio.math.input
scoreboard players operation #new_count_input itemio.math.input -= #full_stack itemio.math.input
execute store result storage itemio:main.input input.count int 1 run scoreboard players get #new_count_input itemio.math.input
