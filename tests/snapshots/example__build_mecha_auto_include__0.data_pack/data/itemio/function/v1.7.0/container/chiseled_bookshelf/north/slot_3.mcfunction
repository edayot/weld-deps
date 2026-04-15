
                #raw f"$say {slot}, {face}, $(chiseled_bookshelf_args)"
execute store success score #ifitem_3 itemio.math if data block ~ ~ ~ Items[{Slot:3b}]
$execute if score #ifitem_3 itemio.math matches 0 run data modify storage itemio:main temp.chiseled_bookshelf_args set value "slot_3_occupied=false,$(chiseled_bookshelf_args)"
$execute if score #ifitem_3 itemio.math matches 1 run data modify storage itemio:main temp.chiseled_bookshelf_args set value "slot_3_occupied=true,$(chiseled_bookshelf_args)"
