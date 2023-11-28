import { useLocation, useParams } from "react-router-dom"

/**
 * 
 * @returns 
 */
export const usePath = () => {
    const { pathname } = useLocation()
    const { id } = useParams()
    let link = pathname
    let hasEdit = false
    if (pathname.includes("edit")) {
        link = pathname.replaceAll("edit/" + id, id)
        hasEdit = true
    } else {
        link = pathname.replaceAll(id, "edit/" + id)    
    }
    const result = {
        editlink: link, 
        editting: hasEdit, 
        linkto: ({name, id}) => {
            const segments = pathname.split('/')
            segments[1] = name
            segments[segments.length-1] = `${id}`
            return segments.join('/')
        }
    }
    console.log("usePath", pathname, id)
    console.log("usePath:", result.linkto({name: "users", id: "1202fc8d-fe0e-41a6-96a6-2009738bc62a"}))
    return result
}
