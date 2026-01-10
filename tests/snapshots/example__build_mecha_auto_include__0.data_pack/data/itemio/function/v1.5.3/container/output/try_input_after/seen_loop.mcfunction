
# @public
#tellraw @p [{"text":"try input after : "},{"nbt":"output","storage":"itemio:io"}]

# Test if the seen_item is in the list of already seen items

scoreboard players set #valid_item itemio.math 0
execute store result score #!same_item itemio.math run data modify storage itemio:main temp.seen_items_loop[0] set from storage itemio:main temp.seen_item

execute if score #!same_item itemio.math matches 0 run return run scoreboard players set #already_seen itemio.math 1

data remove storage itemio:main temp.seen_items_loop[0]
execute if data storage itemio:main temp.seen_items_loop[0] run function itemio:v1.5.3/container/output/try_input_after/seen_loop
