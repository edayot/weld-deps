scoreboard players set #nbt_items itemio.math.output 0
execute if score #good_context_entity itemio.math.output matches 1 if entity @s[tag=itemio.container.nbt_items] run scoreboard players set #nbt_items itemio.math.output 1
data remove storage itemio:main.output Items
data remove storage itemio:main.output nbt_items_path
data modify storage itemio:main.output nbt_items_path set value "storage do_not_use:realy blabla"
execute if score #nbt_items itemio.math.output matches 0 run data modify storage itemio:main.output Items set from block ~ ~ ~ Items
execute if score #nbt_items itemio.math.output matches 1 run function itemio:v1.0.0/container/output/custom/nbt_items_repart
data remove storage itemio:main.output Items[{components: {"minecraft:custom_data": {itemio: {gui: 1b}}}}]
data remove storage itemio:main.output input
data modify storage itemio:main.output input set from storage itemio:io input
data remove storage itemio:io output
data modify storage itemio:main.output filters set value []
data modify storage itemio:main.output filters set from storage itemio:io filters
scoreboard players set #if_item_input itemio.math.output 0
scoreboard players set #if_filters_define itemio.math.output 0
execute store result score #if_filters_define itemio.math.output if data storage itemio:main.output filters[0]
execute store result score #if_item_input itemio.math.output if data storage itemio:main.output input
data remove storage itemio:main.output temp.args_loop_ioconfig
data modify storage itemio:main.output temp.args_loop_ioconfig.output_side set from storage itemio:io output_side
execute if score #nb_entities itemio.math.output matches 1 if data storage itemio:main.output ioconfig[0] run function itemio:v1.0.0/container/output/custom/output_noconfig/loop_ioconfig with storage itemio:main.output temp.args_loop_ioconfig
