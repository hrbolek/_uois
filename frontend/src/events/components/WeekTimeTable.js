export const SVGEvent = (props) => {
    const { XDelta, YDelta, fillColor, lesson, subject, teacher, room } = props
    return (
        <>
            <rect x={XDelta} y={YDelta} width="180" height="100" stroke="#f7b4b7" strokeWidth="1" fill={fillColor}></rect>
            <text fontFamily="Calibri,Calibri_MSFontService,sans-serif" fontWeight="600" fontSize="15" transform={"translate(" + (XDelta + 5) + " " + (YDelta + 14) +")"}>
                <a href={"/ui/studyprograms/subject/" + lesson.id} target="_top">{lesson.name}</a>
                <tspan fontSize="15" fontWeight="400" x="-0.0424118" y="18"><a href={"/ui/studyprograms/subject/" + subject.id} target="_top"></a>{subject.name}</tspan>
                <tspan fontSize="15" fontWeight="400" x="1.04089" y="38"><a href={"/ui/users/teacher/" + teacher.id} target="_top">{teacher.name + " " + teacher.surname }</a></tspan>
                <tspan fontSize="15" fontWeight="400" x="1.04089" y="58"><a href={"/ui/areals/room/" + room.id} target="_top">{room.name}</a></tspan>
                <tspan fontSize="15" fontWeight="400" x="1.04089" y="78"><a href={"/ui/areals/room/" + room.id} target="_top">skupina</a></tspan>
            </text>
        </>
    )
}

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

export const WeekTimeTable = (props) => {
    //meritko je v ose x jedna minuta         -> 2 body
    //           v ose y jeden den            -> 100 bodu
    //referencnim bodem je cas 8:00 prvni den -> (0, 0)
    return (
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" overflow="hidden" viewBox="-61 -26 1500 550">
         <g>
                <SVGTime Xdelta={0} HourValue={"8:00"} />
                <SVGTime Xdelta={220} HourValue={"9:50"} />
                <SVGTime Xdelta={440} HourValue={"11:40"} />
                <SVGTime Xdelta={780} HourValue={"14:30"} />
                <SVGTime Xdelta={1000} HourValue={"16:20"} />
                <SVGTime Xdelta={1200} HourValue={"18:00"} />

                <SVGDate YDelta={0} DateValue={"8.11."} DayValue={"po"}/>
                <SVGDate YDelta={100} DateValue={"9.11."} DayValue={"út"}/>
                <SVGDate YDelta={200} DateValue={"10.11."} DayValue={"st"}/>
                <SVGDate YDelta={300} DateValue={"11.11."} DayValue={"čt"}/>
                <SVGDate YDelta={400} DateValue={"12.11."} DayValue={"pá"}/>

                <SVGEvent XDelta={780} YDelta={300} fillColor={"#f7b4b7"}
                    lesson={{name: "konzultace", id: "1"}} 
                    subject={{name: "", id: "1"}} 
                    teacher={{name: "Michal", surname: "Svoboda", id: "1"}} 
                    room={{name: "", id: "1"}} />
                <SVGEvent XDelta={220} YDelta={100} fillColor={"#b6bd82"}
                    lesson={{name: "Letecké elektronické systémy", id: "1"}} 
                    subject={{name: "3. Syntéza kmitočtu", id: "1"}} 
                    teacher={{name: "Michal", surname: "Svoboda", id: "1"}} 
                    room={{name: "Č1/120", id: "1"}} />
                <SVGEvent XDelta={220} YDelta={400} fillColor={"#b6bd82"}
                    lesson={{name: "Letecké elektronické systémy", id: "1"}} 
                    subject={{name: "3. Syntéza kmitočtu", id: "1"}} 
                    teacher={{name: "Michal", surname: "Svoboda", id: "1"}} 
                    room={{name: "Č1/120", id: "1"}} />
                <SVGEvent XDelta={0} YDelta={300} fillColor={"#859be9"}
                    lesson={{name: "Mentoring studentů 1. ročníku", id: "1"}} 
                    subject={{name: "", id: "1"}} 
                    teacher={{name: "Jana", surname: "Svobodová", id: "1"}} 
                    room={{name: "Č1/120", id: "1"}} />

                
            </g>
        </svg>        
    )
}