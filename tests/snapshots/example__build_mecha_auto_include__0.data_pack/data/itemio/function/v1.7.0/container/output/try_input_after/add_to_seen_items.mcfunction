
# @public
#tellraw @p [{"text":"try input after : "},{"nbt":"output","storage":"itemio:io"}]

# Test if the seen_item is in the list of already seen items

scoreboard players set #remove_count itemio.math.output 0
data modify storage itemio:main.output seen_items append from storage itemio:main temp.seen_item
