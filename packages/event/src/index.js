import { Route  } from 'react-router-dom';

import { EventPage } from "./Pages/EventPage";
import { EventEditPage } from "./Pages/EventEditPage";
import { EventPlanEditPage }  from "./Pages/EventPlanEditPage"

export { EventPage } from "./Pages/EventPage";
export { EventEditPage } from "./Pages/EventEditPage";
export { EventCard } from "./Components/EventCard";
export { EventCalendar } from "./Components/EventCalendar";
export { EventAddDialog } from "./Components/EventAddDialog";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/events/edit/:id"} element={<EventEditPage />} />
            <Route path={"/ui/events/:id"} element={<EventPage />} />
            <Route path={"/ui/events"} element={<EventPlanEditPage />} />
        </>
    )
}

export default Pages