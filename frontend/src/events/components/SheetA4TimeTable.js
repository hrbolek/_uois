import { useMemo, useState, useEffect } from "react"
import { Card } from "react-bootstrap"

import { StudentGroupEvents } from 'events/queries/StudentGroupEvents'

export const SVGTime = (props) => {
    const { Xdelta, HourValue } = props
    return (
        <>
            <rect x={Xdelta} y="-25" width="180" height="25" stroke="#000000" strokeWidth="1" fill="#FFFFFF"></rect>
            <text fontFamily="Calibri,Calibri_MSFontService,sans-serif" fontWeight="600" fontSize="18" transform={"translate(" + (Xdelta + 5) +" -10)"}>
                {HourValue}
            </text>
        </>
    )
}

export const SVGDate = (props) => {
    const { YDelta, DateValue, DayValue } = props
    return (
        <>
            <rect x="-60" y={YDelta} width="60" height="100" stroke="#000000" strokeWidth="1" fill="#FFFFFF"></rect>
            <text fontFamily="Calibri,Calibri_MSFontService,sans-serif" fontWeight="600" fontSize="18" transform={"translate(-58 " + (YDelta + 20) + ")"}>
                {DateValue}
                <tspan fontSize="18" fontWeight="400" x="-0.0424118" y="23">{DayValue}</tspan>
            </text>
        </>
    )
}

export const SVGEvent = (props) => {
    const { XDelta, YDelta, Width, Height, fillColor, lesson, subject, teacher, room, group } = props
    return (
        <>
            <rect x={XDelta} y={YDelta} width={Width} height={Height} stroke="#f7b4b7" strokeWidth="1" fill={fillColor}></rect>
            <text fontFamily="Calibri,Calibri_MSFontService,sans-serif" fontWeight="600" fontSize="15" transform={"translate(" + (XDelta + 5) + " " + (YDelta + 14) +")"}>
                <a href={"/ui/studyprograms/subject/" + lesson.id} target="_top">{lesson.name}</a>
                <tspan fontSize="15" fontWeight="400" x="-0.0424118" y="18"><a href={"/ui/studyprograms/subject/" + subject.id} target="_top"></a>{subject.name}</tspan>
                <tspan fontSize="15" fontWeight="400" x="1.04089" y="38"><a href={"/ui/users/teacher/" + teacher.id} target="_top">{teacher.name + " " + teacher.surname }</a></tspan>
                <tspan fontSize="15" fontWeight="400" x="1.04089" y="58"><a href={"/ui/areals/room/" + room.id} target="_top">{room.name}</a></tspan>
                <tspan fontSize="15" fontWeight="400" x="1.04089" y="78"><a href={"/ui/groups/" + group.id} target="_top">{group.name}</a></tspan>
            </text>
        </>
    )
}

const beginOfWeek = (date) => {
    const delta = date.getDay()
    const result = new Date(date)
    result.setDate(result.getDate() - 6 - delta);
    return result;
}

const endOfWeek = (date) => {
    const delta = date.getDay()
    const result = new Date(date)
    result.setDate(result.getDate() + 1 - delta);
    return result;
}

const addDays = (date, delta) => {
    const result = new Date(date)
    result.setDate(result.getDate() + delta);
    return result;
}


export const SVGTimeTable = (props) => {
    const { startDate, events } = props
    console.log(startDate)
    const days = [0, 1, 2, 3, 4]

    //meritko je v ose x jedna minuta         -> 2 body
    //           v ose y jeden den            -> 100 bodu
    const dayHeight = 100
    //referencnim bodem je cas 8:00 prvni den -> (0, 0)
    return (
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" overflow="hidden" viewBox="-61 -26 1400 550">
         <g>
                <SVGTime Xdelta={0} HourValue={"8:00"} />
                <SVGTime Xdelta={220} HourValue={"9:50"} />
                <SVGTime Xdelta={440} HourValue={"11:40"} />
                <SVGTime Xdelta={780} HourValue={"14:30"} />
                <SVGTime Xdelta={1000} HourValue={"16:20"} />
                <SVGTime Xdelta={1200} HourValue={"18:00"} />

                {days.map(
                    (d, index) => {
                        const currentDay = addDays(startDate, index)
                        const DateValue = currentDay.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
                        const DayValue = currentDay.toLocaleDateString(undefined, { weekday: 'short' })
                        return (
                            <SVGDate key={d} YDelta={0 + index * dayHeight} DateValue={DateValue} DayValue={DayValue}/>
                        )
                    }
                )}


                {events.map(
                    (event, index) => {
                        console.log(JSON.stringify(event))
                        const startDate = new Date(event.startdate)
                        const startDateDay = startDate.getDay() - 1
                        const startMinutes = startDate.getHours() * 60 + startDate.getMinutes() - 8 * 60
                        const YDelta = startDateDay * dayHeight
                        const XDelta = startMinutes * 2
                        const endDate = new Date(event.enddate)
                        const endDateDay = endDate.getDay() - 1
                        const endMinutes = endDate.getHours() * 60 + endDate.getMinutes() - 8 * 60
                        const Width = endMinutes * 2 - startMinutes * 2
                        console.log(YDelta, YDelta)
                        return (
                            <SVGEvent key={event.id} XDelta={XDelta} YDelta={YDelta} Width={Width} Height={dayHeight} fillColor={"#ff7f7f"}
                                lesson={{name: "fsd", id: "1"}} 
                                subject={{name: "", id: "1"}} 
                                teacher={event.organizers[0]} 
                                room={{name: "", id: "1"}} 
                                group={event.groups[0]}/>
                        )
                    }

                )}
               
            </g>
        </svg>        
    )
}

const today = new Date()
export const SVGTimeTableG = (props) => {
    const {group} = props
    const [{startDate, endDate}, setDateInterval]  = useState({startDate: beginOfWeek(today), endDate: endOfWeek(today)})
    const [events, setEvents] = useState([])
    useEffect(()=>{
        StudentGroupEvents(group.id, startDate, endDate)
        .then(response => response.json())
        .then(json => json.data.events)
        .then(events => setEvents(events))
    }, [props.id])
    return (
        <SVGTimeTable startDate={startDate} events={events} />
    )
}



export const SheetA4Week = (props) => {
    const { XDelta, YDelta, startDate, events } = props
    const mondayDate = beginOfWeek(startDate)
    const splitedEvents = useMemo(() => {
        const days = {0:[], 1:[], 2:[], 3: [], 4: []};
        
        for (const property in days) {
            const startDate = addDays(mondayDate, property)
            const endDate = addDays(mondayDate, property+1)
            days[property] = events.filter(e => (e.startdate <= startDate) & (e.enddate <= endDate))
        }

        return days
    }, [startDate, events])
    
    const days = [0, 1, 2, 3, 4]
    const dayHeight = 200
    return (
        <>
            <rect x={XDelta} y={YDelta} width="20" height={dayHeight * days.length} stroke="#000000" strokeWidth="1" fill="#FFFFFF">
            </rect>
            {days.map((item, index) => 
                <SheetA4WeekDay key={index} XDelta={XDelta} YDelta={YDelta + index * dayHeight} 
                    DateValue={item} events={splitedEvents[item]} startDate={addDays(mondayDate, item)}/>
            )}
        </>
    )
}

export const SheetA4WeekDayLesson = (props) => {
    const { XDelta, YDelta, DateValue } = props

    /*
            <text fontFamily="Calibri,Calibri_MSFontService,sans-serif" fontWeight="600" fontSize="5" transform={"translate(" + (XDelta + 1) + " " + (YDelta + 5) +")"}>
                <a href={"/ui/studyprograms/subject/"} target="_top">Topic</a>
                <tspan fontSize="5" fontWeight="400" x="0" y="6"><a href={"/ui/studyprograms/subject/"} target="_top"></a>Subject</tspan>
                <tspan fontSize="5" fontWeight="400" x="0" y="11"><a href={"/ui/users/teacher/"} target="_top">Teachr</a></tspan>
                <tspan fontSize="5" fontWeight="400" x="0" y="17"><a href={"/ui/areals/room/"} target="_top">Room</a></tspan>
                <tspan fontSize="5" fontWeight="400" x="0" y="23"><a href={"/ui/areals/room/"} target="_top">Group</a></tspan>
            </text>

    */
    return (
        <>
            <rect x={XDelta} y={YDelta} width="20" height="30" stroke="#000000" strokeWidth="1" fill="#FFFFFF"></rect>
        </>

    )
}

export const SheetA4WeekDayEvent = (props) => {
    const { XDelta, YDelta, event } = props
    const startDate = event.startDate
    const startMinutes = startDate.getHours() * 60 + startDate.getMinutes()
    const startYDelta = (startMinutes - 8*60) / 4 // m / 120mins * 30px
    const endDate = event.endtDate
    const endMinutes = endDate.getHours() * 60 + endDate.getMinutes()
    const endYDelta = (endMinutes - 8*60) / 4 // m / 120mins * 30px
    return (
        <>
            <clipPath id={event.id}>
            <rect x={XDelta} y={YDelta+startYDelta} width="20" height={endYDelta-startYDelta}></rect>
            </clipPath>
            <rect x={XDelta} y={YDelta+startYDelta} width="20" height={endYDelta-startYDelta} stroke="#000000" strokeWidth="1" fill="#FFFFFF"></rect>
            <text fontFamily="Calibri,Calibri_MSFontService,sans-serif" fontWeight="600" fontSize="5" 
                transform={"translate(" + (XDelta + 1) + " " + (YDelta + 5) +")"}
                clipPath={`url(${event.id})`}
                >
                <a href={"/ui/studyprograms/subject/"} target="_top">{event.name}</a>
                <tspan fontSize="5" fontWeight="400" x="0" y="6"><a href={"/ui/studyprograms/subject/"} target="_top"></a>Subject</tspan>
                <tspan fontSize="5" fontWeight="400" x="0" y="11"><a href={"/ui/users/teacher/"} target="_top">Teachr</a></tspan>
                <tspan fontSize="5" fontWeight="400" x="0" y="17"><a href={"/ui/areals/room/"} target="_top">Room</a></tspan>
                <tspan fontSize="5" fontWeight="400" x="0" y="23"><a href={"/ui/areals/room/"} target="_top">Group</a></tspan>
            </text>
        </>
    )
}

export const SheetA4WeekDay = (props) => {
    //30px 120min?
    const { XDelta, YDelta, startDate, events } = props
    const hours = [0, 1, 2, 3, 4, 5]
    const intervals = [
        {'s': 8 * 60, 'e': 9 * 60 + 30},
        {'s': 9 * 60 + 50, 'e': 11 * 60 + 20},
        {'s': 11 * 60 + 40, 'e': 13 * 60 + 10},
        {'s': 14 * 60 + 30, 'e': 16 * 60 + 0},
        {'s': 16 * 60 + 10, 'e': 17 * 60 + 40},
    ]
    //        {hours.map((item, index) => <SheetA4WeekDayLesson XDelta={XDelta} YDelta={YDelta + 20 + 30 * index} />)}

    return (
        <>
        <rect x={XDelta} y={YDelta} width="20" height="20" stroke="#000000" strokeWidth="1" fill="#ffcc99"></rect>
        {hours.map((item, index) => <SheetA4WeekDayLesson XDelta={XDelta} YDelta={YDelta + 20 + 30 * index} />)}
        {events.map( e => <SheetA4WeekDayEvent event={e} XDelta={XDelta} YDelta={YDelta}/>)}
        </>
    )
}

export const SheetA4Date = (props) => {
    const { YDelta } = props
    return (
        <rect x="-60" y={YDelta} width="60" height="100" stroke="#000000" strokeWidth="1" fill="#FFFFFF"></rect>
    )
}

const createInitializer = (list) => {
    const result = {}
    for(let i of list) {
        result[i] = []
    }
    return result
}

export const SheetA4TimeTable = (props) => {
    const { startDate, events } = props
    
    const weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    const mondayDate = beginOfWeek(startDate)
    const splitedEvents = useMemo(() => {
        
        const weeksSplited = createInitializer(weeks);
        
        for (const property in weeksSplited) {
            const startDate = addDays(mondayDate, property)
            const endDate = addDays(mondayDate, property + 7)
            weeksSplited[property] = events.filter(e => (e.startdate <= startDate) & (e.enddate <= endDate))
        }
    }, [startDate, events])


    return (
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" overflow="hidden" viewBox="-61 -26 500 1400">
            <g>
                <SheetA4Week XDelta={-50} YDelta={0} startDate={mondayDate}  events={[]}/>
                <SheetA4Week XDelta={-30} YDelta={0} startDate={mondayDate}  events={[]}/>
                {weeks.map(
                    (item, index) => <SheetA4Week XDelta={index * 20} YDelta={0} startDate={addDays(mondayDate, index * 7)} events={splitedEvents[item]}/> 
                )}
            </g>
        </svg> 
    )
}