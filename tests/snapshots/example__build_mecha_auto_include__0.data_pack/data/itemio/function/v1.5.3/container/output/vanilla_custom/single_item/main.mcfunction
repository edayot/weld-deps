
execute unless data storage itemio:main.output ItemUnique run return fail

data remove storage itemio:main.output input
data modify storage itemio:main.output input set from storage itemio:io input
data remove storage itemio:io output

scoreboard players set #if_item_input itemio.math.output 0
scoreboard players set #if_filters_define itemio.math.output 0
execute store result score #if_item_input itemio.math.output if data storage itemio:main.output input
execute store result score #if_filters_define itemio.math.output if data storage itemio:io filters[0]

data modify storage itemio:main.output filters set from storage itemio:io filters

execute if score #if_filters_define itemio.math.output matches 1 run function itemio:v1.5.3/container/output/vanilla_custom/single_item/main/check_filters

execute if score #if_filters_define itemio.math.output matches 0 if score #if_item_input itemio.math.output matches 1 run function itemio:v1.5.3/container/output/vanilla_custom/single_item/main/check_item_input

execute if score #if_filters_define itemio.math.output matches 0 if score #if_item_input itemio.math.output matches 0 run function itemio:v1.5.3/container/output/vanilla_custom/single_item/main/output

        #check maxcount
