import { FormComponent } from "./FormTypes"

export const FormCardBody = ({form, mode}) => {
    const Visualiser = FormComponent(form)
    return (
        <Visualiser form={form} mode={mode}/>
    )
}