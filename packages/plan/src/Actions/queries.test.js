// const fetch = require('node-fetch')
import fetch from 'node-fetch'
import { PlanQuery } from "./PlanFetchAsyncAction"
import { LessonRemoveTeacherQuery } from "./LessonRemoveTeacherAsyncAction"

global.fetch = (path, params) => fetch("http://localhost:31180" + path, params)

// const { PlanQuery } = require("./PlanFetchAsyncAction")

const GetJSON = (response) => response.json()

const CheckNoError = (json) => {
    expect(json.errors).toBeUndefined()
    expect(json.data.result).not.toBeUndefined()
    return json
}

const CheckMsgOk = (json) => {
    expect(json.data.result.msg).not.toBeUndefined()
    expect(json.data.result.msg).toBe("ok")
    return json
}

const CheckId = (id) => (json) => {
    expect(json.data.result.id).toBe(id)
    return json
}

test('planById', () => {
    const id = "a5085468-394f-4a8b-bf23-4e72a6a6d415"
    return PlanQuery(id)
        .then(GetJSON)
        .then(CheckNoError)
        .then(CheckId(id))
});

test('LessonRemoveTeacherQuery', () => {
    const user_id = "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"
    const lesson_id = "704e7bc2-b1d6-4fe3-95ce-b008b352dd59"
    return LessonRemoveTeacherQuery({user_id, lesson_id})
        .then(GetJSON)
        .then(CheckNoError)
        .then(CheckMsgOk)
        .then(CheckId(lesson_id))
});


