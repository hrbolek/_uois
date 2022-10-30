import { createSlice } from '@reduxjs/toolkit';


const extraProps = {
    "id": "4e3b3503-5d20-458b-9f4d-fd7f35306ee0",
    "name": "University of IT",
    "roles": [
      {
        "roletype": {
          "name": "rector"
        },
        "user": {
          "name": "Marie Václav",
          "surname": "Černý",
          "email": "Marie.Václav.Černý@university.world"
        }
      },
      {
        "roletype": {
          "name": "vicerector"
        },
        "user": {
          "name": "Pavel Jan",
          "surname": "Černý",
          "email": "Pavel.Jan.Černý@university.world"
        }
      },
      {
        "roletype": {
          "name": "vicerector"
        },
        "user": {
          "name": "Eva Václav",
          "surname": "Dvořák",
          "email": "Eva.Václav.Dvořák@university.world"
        }
      },
      {
        "roletype": {
          "name": "vicerector"
        },
        "user": {
          "name": "Hana Milan",
          "surname": "Nováková",
          "email": "Hana.Milan.Nováková@university.world"
        }
      },
      {
        "roletype": {
          "name": "vicerector"
        },
        "user": {
          "name": "Miroslav Věra",
          "surname": "Pokorná",
          "email": "Miroslav.Věra.Pokorná@university.world"
        }
      }
    ],
    "mastergroup": null
  }


export const groupSlice = createSlice({
    name: 'group',
    initialState: {'id': null},
    reducers: {
      setGroup: (state, action) => ({...state, ...action.payload}),
    },
  })


const updateGroup = async (group) => {
    const response = await fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!, $group: GroupUpdateGQLModel!) {
                    groupById(id: $id) {
                        editor {
                            update(group: $group) {
                                id 
                                name
                                grouptype {
                                    id
                                    name
                                }
                            }
                        }
                    }
                }`,
            "variables": {"id": group.id, "group": {...group, id: null}} //group substructure cannot have id
        }),
    })
    const data = await response.json()
    return data.group.groupById.editor.update
}

const fetchDepartment = async (id) => {
    const response = await fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                      id
                      name
                      roles {
                        roletype {
                          name
                        }
                        user {
                          name
                          surname
                          email
                        }
                      }
                      memberships {
                        user {
                          id
                          name
                          surname
                          email
                        }
                      }
                      mastergroup {
                        id
                        name
                        grouptype {
                          name
                        }
                        mastergroup {
                          id
                          name
                          grouptype {
                            name
                          }
                          mastergroup {
                            id
                            name
                            grouptype {
                              name
                            }
                          }
                        }
                      }
                    }
                  }`,
            "variables": {"id": id}
        }),
    })
    const data = await response.json()
    return data.groupById
}

const fetchGroup = async (id) => {
    const response = await fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                      id
                      name
                      roles {
                        roletype {
                          name
                        }
                        user {
                          name
                          surname
                          email
                        }
                      }
                      mastergroup {
                        id
                        name
                        grouptype {
                          name
                        }
                        mastergroup {
                          id
                          name
                          grouptype {
                            name
                          }
                          mastergroup {
                            id
                            name
                            grouptype {
                              name
                            }
                          }
                        }
                      }
                    }
                  }`,
            "variables": {"id": id}
        }),
    })
    const data = await response.json()
    return data.groupById
}


const fetchGroupMembers = async (id) => {
    const response = await fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                      memberships {
                        user {
                          id
                          name
                          surname
                          email
                        }
                      }
                    }
                  }`,
            "variables": {"id": id}
        }),
    })
    const data = await response.json()
    return data.groupById
}

export function updateGroupAction(group) {
    return async function (dispatch, getState) {
        const response = await updateGroup(group)
        dispatch(groupSlice.actions.setGroup(response))
    }
}

export function fetchGroupAction(group) {
    return async function (dispatch, getState) {
        const response = await fetchGroup(group.id)
        dispatch(groupSlice.actions.setGroup(response))
    }
}

export function fetchDepartmentAction(group) {
    return async function (dispatch, getState) {
        const responseA = await fetchGroup(group.id)
        const responseB = await fetchGroupMembers(group.id)
        dispatch(groupSlice.actions.setGroup({...responseA, ...responseB}))
    }
}
