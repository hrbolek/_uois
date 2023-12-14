import ReactDatePicker, { registerLocale } from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css";
import cs from 'date-fns/locale/cs';
import { forwardRef } from "react";
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

/**
 * 
 * @param {*} selected datetime initial value
 * @param {*} onChange callback called when datetime has changed
 * @returns JSX.Element Button like datetime picker
 */
export const DatePicker = ({selected, onChange}) => {
    const onChange_ = (value) => {
        const iso = value.toISOString().replace('Z', '')
        if (onChange) {
            onChange(iso)
        }
    }
    let cdate = null
    if (selected) {
        cdate = new Date(selected + 'Z')
        // console.log("cdate.selected", selected)
        // console.log("cdate.cdate", cdate)
        //cdate = new Date()
    } else {
        cdate = null
    } 
    // const cdate = selected ? new Date(selected + 'Z'): null
    // console.log("cdate.selected", selected)
    // console.log("cdate.cdate", cdate)
    return (
        <ReactDatePicker selected={cdate} onChange={onChange_} 
        dateFormat="dd.MM.yyyy" locale="cs" customInput={<ExampleCustomInput />}/>
    )
}