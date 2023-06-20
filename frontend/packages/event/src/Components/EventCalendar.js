import FullCalendar from '@fullcalendar/react' // must go before plugins
import dayGridPlugin from '@fullcalendar/daygrid' // a plugin!
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import csLocale from '@fullcalendar/core/locales/cs';

import { sliceEvents, createPlugin } from '@fullcalendar/core';

export const CustomView = (props) => {
    let segs = sliceEvents(props, true); // allDay=true

    return (
      <>
        <div className='view-title'>
          {props.dateProfile.currentRange.start.toUTCString()}
        </div>
        <div className='view-events'>
          {segs.length} events
        </div>
      </>
    );


}

const localPlugin = createPlugin({
  views: {
    custom: CustomView
  }
});

let todayStr = new Date().toISOString().replace(/T.*$/, '') // YYYY-MM-DD of today

let eventGuid = 0 
function createEventId() {
    return String(eventGuid++)
  }

const INITIAL_EVENTS = [
  {
    id: createEventId(),
    title: 'All-day event',
    start: todayStr
  },
  {
    id: createEventId(),
    title: 'Timed event',
    start: todayStr + 'T12:00:00'
  }
]

export const EventCalendar = ({events, onSelect}) => {

    const handleDateSelect = (selectInfo) => {
        if (onSelect) {
            onSelect(selectInfo)
        }
      }
    
    const  handleEventClick = (clickInfo) => {
        
          clickInfo.event.remove()
        
      }
    const renderEventContent = (eventInfo) => {
    return (
        <>
            <b>{eventInfo.timeText}</b>
            <i>{eventInfo.event.title}</i>
        </>
    )
    }
    
    return (
        <>
        <hr/>
        Kalendar
        <FullCalendar 
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin, localPlugin]}
            initialView='timeGridWeek'
            // initialView={"custom"}
            locale={csLocale}

            weekends={false}
            editable={true}
            selectable={true}
            events={events}
            initialEvents={INITIAL_EVENTS}

            select={handleDateSelect}
            // eventContent={renderEventContent} // custom render function
            eventClick={handleEventClick}

            eventAdd={function(){}}
            eventChange={function(){}}
            eventRemove={function(){}}
        />
        {JSON.stringify(events)}
        <hr/>
        </>
    )
}