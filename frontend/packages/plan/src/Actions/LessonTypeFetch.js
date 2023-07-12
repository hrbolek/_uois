import { CreateFetchQuery } from "@uoisfrontend/shared/src/Queries"

export const LessonTypeQueryJSON = ({skip=0, limit=100}) => ({
    query: `
        query {
            result: aclessonTypePage {
            id
            name
            }
        }    
    `,
    variables: {}
})

export const LessonTypeFetch = CreateFetchQuery(LessonTypeQueryJSON)