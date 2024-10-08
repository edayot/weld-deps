####################
# Commands to total the extra shift-clicked items needed
####################

# Find the total number of output items needed
scoreboard players set $temp2 smithed.data 1000
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 2b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 3b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 4b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 11b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 12b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 13b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 20b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 21b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot: 22b}].count
execute if score @s smithed.data matches 1.. if score @s smithed.data < $temp2 smithed.data run scoreboard players operation $temp2 smithed.data = @s smithed.data

scoreboard players remove $temp2 smithed.data 1
execute if score $temp2 smithed.data matches 1..64 run function smithed.crafter:v0.4.0/block/table/crafting/output/shift_click/calculate_extras
