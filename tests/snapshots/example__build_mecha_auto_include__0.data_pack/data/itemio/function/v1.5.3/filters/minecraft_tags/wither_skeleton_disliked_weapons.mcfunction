
scoreboard players set #filter.valid_item itemio.io 0
data remove entity @s item
data modify entity @s item set from storage itemio:io item
execute if items entity @s container.0 #wither_skeleton_disliked_weapons run scoreboard players set #filter.valid_item itemio.io 1
