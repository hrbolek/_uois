import { Main as Master, MainTabbed } from "./BezTypu/Main"
import { Main as ZadostVolno } from "./ZadostVolno/Main"


import { MasterItem } from "../ItemTypes/MasterItem"
import { StudentItem } from "../ItemTypes/StudentItem"
import { MultiLineItem } from "../ItemTypes/MultilineTextItem"
const formIndex = {
    "2e1140f4-afb0-11ed-9bd8-0242ac110002" : ZadostVolno
}

export const FormComponent = ({type}) => {
    console.log("FormComponent", type)
    let Result = Master
    if (type?.id) {
        Result = formIndex[type?.id] || Master
    }

    // return Result
    return MainTabbed
}

const itemIndex = {
    "9bdb916a-afb6-11ed-9bd8-0242ac110002": StudentItem,
    "9bdb9426-afb6-11ed-9bd8-0242ac110002": MultiLineItem
}

export const ItemComponent = ({type}) => {
    console.log("ItemComponent", type)
    let Result = MasterItem
    if (type?.id) {
        Result = itemIndex[type?.id] || MasterItem
    }

    return Result
}