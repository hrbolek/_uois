import All from "@uoisfrontend/shared/src/keyedreducers";
import { UserEventsQuery } from "../Queries/UserEventsQuery"
import { UserFetchAsyncAction } from "./UserFetchAsyncAction";

const adddays = (d, days) => {
    return new Date(d.valueOf() + 24*60*60*days)
}

export const UserEventsFetchAsyncAction = (user, startdate, enddate) => (dispatch, getState) => {
    // const _startdate = startdate || adddays(new Date(), - 1)
    // const _enddate = enddate || adddays(new Date(), +3)
    let _startdate = startdate || new Date('2023-01-01');
    let _enddate = enddate || new Date('2023-12-31');

    _startdate = _startdate.toISOString().slice(0, -1);
    _enddate = _enddate.toISOString().slice(0, -1);

    return UserEventsQuery(user, _startdate, _enddate)
    .then(response => response.json())
    .then(
        json => {
            const result = json?.data?.result
            if (result) {
                // console.log("UserEventsFetchAsyncAction")
                // console.log("UserEventsFetchAsyncAction", result["events"])
                const action = All.ItemSliceActions.item_updateAttributeVector({item: result, vectorname: "events"})
                dispatch(action)
            }
            return json
        }
    )
}