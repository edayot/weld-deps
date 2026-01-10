
data remove storage itemio:io filters
data modify storage itemio:io filters set from storage itemio:main.output filters
data modify storage itemio:io item set from storage itemio:main.output ItemUnique

function #itemio:calls/filters_v2

execute if score #filters.valid_item itemio.io matches 1 run function itemio:v1.5.3/container/output/vanilla_custom/single_item/main/output

        #check maxcount
