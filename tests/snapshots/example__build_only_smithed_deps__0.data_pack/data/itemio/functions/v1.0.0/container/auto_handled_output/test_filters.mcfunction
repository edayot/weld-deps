data remove storage itemio:io item
data modify storage itemio:io item set from storage itemio:io Item_auto_output
function #itemio:calls/filters_v2
execute if score #filters.valid_item itemio.io matches 1 run function itemio:v1.0.0/container/auto_handled_output/output
