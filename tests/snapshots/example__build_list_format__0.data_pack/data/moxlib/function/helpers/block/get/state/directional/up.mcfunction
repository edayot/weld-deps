execute if predicate moxlib:block/states/up/true run data modify storage moxlib:api/helpers/block/get output.state.up set value true
execute if predicate moxlib:block/states/up/false run data modify storage moxlib:api/helpers/block/get output.state.up set value false