
# @public
# These are example of integrated filter
# Remember : Do not modify any of the input data 

# Inputs :
# storage itemio:io filter
# storage itemio:io item

# Outputs :
# score #filter.valid_item itemio.math
# The score is 1 if the item is valid and act as an AND gate for all the filters

execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.energy run function itemio:v1.5.3/filters/energy
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.id run function itemio:v1.5.3/filters/id
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.ctc run function itemio:v1.5.3/filters/ctc
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.smithed.id run function itemio:v1.5.3/filters/smithed_id
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.merge as a97c9c67-fde0-4b89-926d-54fa4a866004 run function itemio:v1.5.3/filters/merge
execute if score #filter.valid_item itemio.io matches 1 if data storage itemio:io filter.item_predicate as a97c9c67-fde0-4b89-926d-54fa4a866004 run function itemio:v1.5.3/filters/item_predicate with storage itemio:io filter
function itemio:v1.5.3/filters/minecraft_tags

#tellraw @a {"score":{"name":"#filter.valid_item","objective":"itemio.io"}}
