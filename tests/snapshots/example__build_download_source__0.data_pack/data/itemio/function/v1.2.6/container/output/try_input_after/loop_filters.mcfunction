data remove storage itemio:io filters
data modify storage itemio:io filters set from storage itemio:main servo_filters2
data remove storage itemio:io item
data modify storage itemio:io item set from storage itemio:io output
function #itemio:calls/filters_v2
scoreboard players set #success_input itemio.io 0
execute if score #filters.valid_item itemio.io matches 1 run function itemio:v1.2.6/container/output/try_input_after/input
