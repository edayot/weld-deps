
scoreboard players set #nbt_items itemio.math.input 0
execute if score #good_context_entity itemio.math.input matches 1 if entity @s[tag=itemio.container.nbt_items] run scoreboard players set #nbt_items itemio.math.input 1

#loading block data
data remove storage itemio:main.input Items
data remove storage itemio:main.input nbt_items_path
data modify storage itemio:main.input nbt_items_path set value "storage do_not_use:realy blabla"
execute if score #nbt_items itemio.math.input matches 0 run data modify storage itemio:main.input Items set from block ~ ~ ~ Items
execute if score #nbt_items itemio.math.input matches 1 run function itemio:v1.5.3/container/input/custom/nbt_items_repart

data remove storage itemio:main.input Items[{components: {"minecraft:custom_data": {itemio: {gui: 1b}}}}]
data remove storage itemio:main.input input
data modify storage itemio:main.input input set from storage itemio:io input

scoreboard players set #test_side itemio.math.input 0

execute if score #nbt_items itemio.math.input matches 1 if score #nb_entities itemio.math.input matches 1 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "north"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/north

execute if score #nbt_items itemio.math.input matches 0 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "north"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/north
execute if score #nbt_items itemio.math.input matches 1 if score #nb_entities itemio.math.input matches 1 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "south"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/south
execute if score #nbt_items itemio.math.input matches 0 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "south"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/south
execute if score #nbt_items itemio.math.input matches 1 if score #nb_entities itemio.math.input matches 1 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "east"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/east
execute if score #nbt_items itemio.math.input matches 0 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "east"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/east

execute if score #nbt_items itemio.math.input matches 1 if score #nb_entities itemio.math.input matches 1 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "west"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/west
execute if score #nbt_items itemio.math.input matches 0 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "west"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/west
execute if score #nbt_items itemio.math.input matches 1 if score #nb_entities itemio.math.input matches 1 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "top"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/top
execute if score #nbt_items itemio.math.input matches 0 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "top"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/top
execute if score #nbt_items itemio.math.input matches 1 if score #nb_entities itemio.math.input matches 1 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "bottom"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/bottom
execute if score #nbt_items itemio.math.input matches 0 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "bottom"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig/bottom
execute if score #nbt_items itemio.math.input matches 1 if score #nb_entities itemio.math.input matches 1 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "wireless"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig
execute if score #nbt_items itemio.math.input matches 0 if score #test_side itemio.math.input matches 0 if data storage itemio:io {input_side: "wireless"} run function itemio:v1.5.3/container/input/custom/input_no_config/loop_ioconfig

data remove storage itemio:io output
data modify storage itemio:io output set from storage itemio:io input
data modify storage itemio:io output.count set from storage itemio:main.input input.count

execute store result score #count_input itemio.math.input run data get storage itemio:io input.count
execute store result score #count_output itemio.math.input run data get storage itemio:io output.count

scoreboard players set #count_to_remove itemio.math.input 0
scoreboard players operation #count_to_remove itemio.math.input = #count_input itemio.math.input
scoreboard players operation #count_to_remove itemio.math.input -= #count_output itemio.math.input

scoreboard players operation #count_to_remove itemio.io = #count_to_remove itemio.math.input
