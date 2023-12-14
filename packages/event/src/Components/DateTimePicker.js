import ReactDatePicker, { setTime, registerLocale } from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css";
import cs from 'date-fns/locale/cs';
import { forwardRef } from "react";
import { useState } from "react";
registerLocale('cs', cs)

const ExampleCustomInput = forwardRef(({ value, onClick }, ref) => {
    if (value) {
        return (
            <button className="btn btn-sm btn-outline-success" onClick={onClick} ref={ref}>
              {value}
            </button>
          )
    } else {
        return (
            <button className="btn btn-sm btn-outline-success" onClick={onClick} ref={ref}>
              {"?"}
            </button>
          )
    }
    });

export const DateTimePicker = ({selected, onChange, startDate, endDate}) => {
    const onChange_ = (value) => {
        const iso = value.toISOString().replace('Z', '')
        if (onChange) {
            onChange(iso)
        }
    }
    const cdate = selected ? new Date(selected + 'Z'): null
    // console.log("cdate.selected", selected)
    // console.log("cdate.cdate", cdate)
    return (
        <ReactDatePicker selected={cdate} onChange={onChange_} 
        dateFormat="dd.MM.yyyy h:mm" locale="cs" customInput={<ExampleCustomInput />} 
        injectTimes={[
            // setTime(new Date(), {hour: 9, minute: 50}),
            // setTime(new Date(), {hour: 11, minute: 20}),
            // setTime(new Date(), {hour: 11, minute: 40}),
            // setTime(new Date(), {hour: 13, minute: 10}),
          ]}
        showTimeSelect
        />
    )
}

export const DateTimePicker_ = ({selected, onChange, startDate, endDate}) => {
    const [startDate_, setStartDate] = useState(new Date());
    const [endDate_, setEndDate] = useState(null);
    const onChange_ = (dates) => {
        console.log(dates)
        // const [start, end] = dates;
        // setStartDate(start);
        // setEndDate(end);
    };
    return (
        <ReactDatePicker
        selected={startDate_}
        onChange={onChange_}
        startDate={startDate_}
        endDate={endDate_}
        selectsRange
        showTimeSelect
        //   inline
        />
    );
}