import { useState } from "react"
import { CalendarFill, CalendarPlusFill, PlusLg, X, XLg } from "react-bootstrap-icons"
import Button from "react-bootstrap/Button"
import Card from "react-bootstrap/Card"
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import { DatePicker, DateTimePicker, Dialog, EditableText, TextInput } from "@uoisfrontend/shared"
import { EventCalendar } from "@uoisfrontend/event"
import { EventAddDialog } from "@uoisfrontend/event"
import { UserSearch } from "../.."



export const UserAddEventDialog = ({user, onClose}) => {
    const onFinish = () => {
        if (onClose) {
            onClose()
        }
    }
    const onCancel = () => {
        if (onClose) {
            onClose()
        }
    }
    const onChangeStart = (isoValue) => {}
    const onChangeEnd = (isoValue) => {}
    return (
        // <GeneralDialog title="Nová událost" oklabel="Ok" cancellabel="Zrušit" onCancel={onCancel} onOk={onFinish} >
        //     <Row>
        //         <Col></Col>
                
                
                
        //         <Col>
        //         <EventCalendar events={[]}/>
        //         </Col>
        //     </Row>
        // </GeneralDialog>
        <></>
    )
}

const FromInfoToNewEventDialog = ({selectInfo, onOk, onCancel}) => {
    const [text, setText] = useState("Nová událost")
    const [startDate, setStartDate] = useState(selectInfo.start)
    const [endDate, setEndDate] = useState(selectInfo.end)

    const onTextChange = (value) => {
        setText(value)
    }
    const onStartChange = (value) => {
        setStartDate(new Date(value + "Z"))
    }
    const onEndChange = (value) => {
        setEndDate(new Date(value + "Z"))
    }

    return (
        <Dialog show title={text} onOk={onOk} onCancel={onCancel}>
            <Row>
                <Col md="2">Start</Col>
                {/* <Col md="10">{JSON.stringify(startDate)}</Col> */}
                <Col md="10"><DateTimePicker selected={startDate.toISOString()} onChange={onStartChange} /></Col>
            </Row>
            <Row>
                <Col md="2">End</Col>
                {/* <Col md="10">{JSON.stringify(endDate)}</Col> */}
                <Col md="10"><DateTimePicker selected={endDate.toISOString()} onChange={onEndChange} /></Col>
            </Row>
            <Row>
                <Col md="2">Název</Col>
                <Col md="10">
                    <TextInput id="2689c9cc-7633-43e2-8e8d-92af25e4c090" value={text} onChange={onTextChange} />
                </Col>
            </Row>
            <Row>
                <Col><br /></Col>
            </Row>
            <Row>
                <Col md="2">Organizátor</Col>
                <Col md="10">
                    <div className="input-group input-group-sm mb-3"> 
                        <span className="btn btn-sm btn-outline-dark">{"John"} {"Newbie"}<X/></span>
                    </div>
                    {/* <TextInput id="2689c9cc-7633-43e2-8e8d-92af25e4c090" value={text} onChange={onTextChange} /> */}
                </Col>
            </Row>
            {/* <Row>
                <Col><br /></Col>
            </Row> */}
            <Row>
                <Col md="2">Povinní </Col>
                <Col md="10">
                    <div className="input-group input-group-sm mb-3">  
                        <span className="btn btn-sm btn-outline-dark">{"Julia"} {"Newbie"}<X/></span>
                        <input className="form-control"/>
                    </div>
                </Col>
                </Row>
            {/* <Row>
                <Col><br /></Col>
            </Row> */}
            <Row>
                <Col md="2">Pozvaní </Col>
                <Col md="10">
                    <div className="input-group input-group-sm mb-3">  
                        <span className="btn btn-sm btn-outline-dark">{"Jepetto"} {"Newbie"}<X/></span>
                        <input className="form-control"/>
                    </div>
                </Col>
            </Row>
            {/* <dl>
                <dd>Start</dd>
                <dt>{JSON.stringify(selectInfo.start)}</dt>
                <dd>End</dd>
                <dt>{JSON.stringify(selectInfo.end)}</dt>
                <dd>Název</dd>
                <dt><TextInput id="2689c9cc-7633-43e2-8e8d-92af25e4c090" value="Nová událost" /></dt>

            </dl> */}
            {/* {JSON.stringify(selectInfo)} */}
        </Dialog>
    )
}

// handleDateSelect = (selectInfo) => {
//     let title = prompt('Please enter a new title for your event')
//     let calendarApi = selectInfo.view.calendar

//     calendarApi.unselect() // clear date selection

//     if (title) {
//       calendarApi.addEvent({
//         id: createEventId(),
//         title,
//         start: selectInfo.startStr,
//         end: selectInfo.endStr,
//         allDay: selectInfo.allDay
//       })
//     }
//   }

export const UserAddEventButton = ({user}) => {
    const onClose = () => {
        setState("button")
    }
    const onOpen = () => {
        setState("dialog")
    }
    
    const [selectInfo, setSelectInfo] = useState(null)
    const confirmNewEvent = () => {
        // let title = prompt('Please enter a new title for your event')
        // let calendarApi = selectInfo.view.calendar
    
        // calendarApi.unselect() // clear date selection
    
        // if (title) {
        //     calendarApi.addEvent({
        //     id: "",
        //     title,
        //     start: selectInfo.startStr,
        //     end: selectInfo.endStr,
        //     allDay: selectInfo.allDay
        //     })
        // }
        setSelectInfo(null)
    }

    const handleDateSelect = (newSelectInfo) => {
        console.log("handleDateSelect", newSelectInfo)
        setSelectInfo(newSelectInfo)
    }

    const [state, setState] = useState("dialog")

    return (
        <>
            ::::::::::::::
            <EventCalendar events={[]}
                onSelect={handleDateSelect}
            />

            {selectInfo?
                <FromInfoToNewEventDialog 
                    selectInfo={selectInfo} 
                    onCancel={()=>setSelectInfo(null)}
                    onOk={()=>confirmNewEvent()}
                />:""}
        </>
        // <Button variant="outline-success" onClick={onOpen}><CalendarPlusFill />Nová událost</Button>
    )


    // if (selectInfo) {}
    // if (state === "button") {
    //     return (
    //         <EventCalendar events={[]}
    //             select={handleDateSelect}
    //         />
    //         // <Button variant="outline-success" onClick={onOpen}><CalendarPlusFill />Nová událost</Button>
    //     )
    // } else {
    //     return <UserAddEventDialog user={user} onClose={onClose} />
    // }

}